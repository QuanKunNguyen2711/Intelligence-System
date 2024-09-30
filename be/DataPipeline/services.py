import asyncio
import json
import re
import time
from typing import List, Tuple
from bson import ObjectId
from fastapi import UploadFile
import pandas as pd
import py_vncorenlp
from pymongo import MongoClient, errors
import concurrent.futures
import math
import os
import logging
import torch
from transformers import AutoTokenizer
from torch.utils.data import DataLoader, random_split
import warnings
from app.common.db_collections import Collections
from app.common.utils import get_current_datetime
from app.common.db_connector import client

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message="`resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`",
)


tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir="/vncorenlp")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Datasets(torch.utils.data.Dataset):
    def __init__(
        self,
        df: pd.DataFrame,
        cols: List[str],
        max_length: int = 256,
    ):
        self.df = df
        self.cols = cols
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return self.df.loc[:, self.cols[-1]].shape[0]

    def __getitem__(self, index):
        inputs = [self.df.iloc[index, i] for i in range(len(self.cols[:-1]))]
        output = self.df.iloc[index, len(self.cols) - 1]

        text = ""
        for i, s in enumerate(inputs):
            if i == len(inputs) - 1:
                text += f"{s}"
                break

            text += f"{s} </s> "

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            return_attention_mask=True,
            truncation=True,
            return_token_type_ids=False,
            return_tensors="pt",
        )

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "label": torch.as_tensor(output, dtype=torch.long),
        }


class DataFrameDataset(torch.utils.data.Dataset):
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        return self.dataframe.iloc[idx]


def get_train_val_test_dataloader(
    df: pd.DataFrame, cols: List[str], batch_size: int = 64
) -> Tuple[DataLoader]:

    train_size = int(0.8 * len(df))
    val_size = int(0.1 * len(df))
    test_size = len(df) - train_size - val_size

    dataset = DataFrameDataset(df)

    train_subset, val_subset, test_subset = random_split(
        dataset,
        [train_size, val_size, test_size],
        generator=torch.Generator().manual_seed(42),
    )
    train_df = subset_to_dataframe(train_subset, df)
    val_df = subset_to_dataframe(val_subset, df)
    test_df = subset_to_dataframe(test_subset, df)

    train_datasets = Datasets(train_df, cols, batch_size)
    val_datasets = Datasets(val_df, cols, batch_size)
    test_datasets = Datasets(test_df, cols, batch_size)

    train_loader = DataLoader(
        train_datasets, batch_size, shuffle=True, num_workers=4, drop_last=True
    )
    val_loader = DataLoader(val_datasets, batch_size, num_workers=4, drop_last=True)
    test_loader = DataLoader(test_datasets, batch_size, num_workers=4, drop_last=True)

    return train_loader, val_loader, test_loader


def subset_to_dataframe(subset, original_dataframe):
    indices = subset.indices
    return original_dataframe.iloc[indices].reset_index(drop=True)


async def preprocess_dataset(
    df: pd.DataFrame, features: List[str], label: str, db_str: str, cur_user_id: str
):
    # Dropout some NaN labels
    filtered_df = df.dropna(subset=[label])

    # features must be text
    filtered_df = filtered_df[filtered_df[label].apply(lambda x: isinstance(x, int))]

    for feature in features:
        filtered_df = filtered_df[
            filtered_df[feature].apply(lambda x: isinstance(x, str))
        ]

    df_features = filtered_df[features]
    df_labels = filtered_df[label]
    logger.info(f"{get_current_datetime()} - Start preprocessing datasets")
    start_t = time.time()

    loop = asyncio.get_event_loop()
    df_features = await loop.run_in_executor(
        None, preprocess_inputs_concurrently, df_features, 4
    )

    df_concat = pd.concat([df_features, df_labels], axis=1)

    # Sample to reduce the size
    score_counts = df_concat[label].value_counts()
    logger.info("Original Score Distribution:")
    logger.info(score_counts)

    # Perform undersampling to balance the dataset
    balanced_df = pd.concat(
        [
            df_concat[df_concat[label] == score].sample(
                min(score_counts), replace=False
            )
            for score in score_counts.index
        ]
    )

    # Reduce the size of the balanced dataset by factor of 0.5
    reduced_size_df = balanced_df.sample(frac=0.5, random_state=42)

    # Check the distribution of scores in the reduced dataset
    reduced_score_counts = reduced_size_df[label].value_counts().sort_index()
    logger.info("\nReduced Score Distribution:")
    logger.info(reduced_score_counts)

    end_t = time.time()
    logger.info(f"{get_current_datetime()} - Preprocessing runtime: {end_t - start_t}")

    config = {"features": features, "label": label}

    first_10_rows = await save_db(
        reduced_size_df,
        db_str,
        config,
    )
    
    return {"result": first_10_rows, "reduced_score": reduced_score_counts.to_dict()}

    # await ws_manager.send_ws(
    #     {"result": first_10_rows, "reduced_score": reduced_score_counts, "event": WebsocketEventResult.PREPROCESS_DATASET},
    #     cur_user_id,
    # )


def divide_df_into_chunks(df: pd.DataFrame, max_threads=4) -> List[pd.DataFrame]:
    num_chunks = math.ceil(len(df) / max_threads)
    return [
        df.iloc[i * num_chunks : (i + 1) * num_chunks]
        for i in range(math.ceil(len(df) / num_chunks))
    ]


def preprocess_inputs_concurrently(
    df: pd.DataFrame, max_threads=os.cpu_count()
) -> pd.DataFrame:
    chunks = divide_df_into_chunks(df, max_threads)
    processed_chunks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_chunk = {
            executor.submit(process_chunk, df_chunk): df_chunk for df_chunk in chunks
        }
        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk = future_to_chunk[future]
            processed_chunk = future.result()
            processed_chunks.append(processed_chunk)

    concat_chunks = pd.concat(processed_chunks)
    concat_chunks = concat_chunks.sort_index()
    concat_chunks.reset_index(inplace=True)
    return concat_chunks


def process_chunk(df_chunk: pd.DataFrame) -> pd.DataFrame:
    df_chunk = df_chunk.applymap(lambda x: process_text(x))
    return df_chunk


def process_text(x):
    if not isinstance(x, str):
        return ""
    return word_segmentation(text_cleaning(x))


def word_segmentation(text: str) -> str:
    output = rdrsegmenter.word_segment(text)
    output = "".join(output)
    return output


def text_cleaning(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"https?://\S+", "", text)
    emoji_pattern = re.compile(
        "["
        # "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub("", text)
    text = re.sub(r"[\s]+", " ", text)
    return text


def get_datasets_from_csa_be(
    client: MongoClient, db_id: str, obj_id_str: str, cols: List[str]
) -> pd.DataFrame:
    db = client.get_database(db_id)
    records_obj = db.get_collection(obj_id_str)
    projection = {col: 1 for col in cols}
    projection.update({"_id": 0})
    docs = list(records_obj.find({}, projection))
    df = pd.DataFrame(docs)
    df = df.fillna("")
    return df


async def save_db(
    df: pd.DataFrame,
    db_id: str,
    config: dict,
) -> List[dict]:
    global client

    _ids = [str(ObjectId()) for _ in range(len(df))]
    df.insert(0, "_id", _ids)

    records = df.to_dict(orient="records")
    total_docs = len(records)

    db = client.get_database(db_id)
    config_coll = db.get_collection(Collections.DATASET_CONFIG)

    if await config_coll.count_documents({}) > 0:
        await config_coll.drop()
        await config_coll.insert_one(
            {"_id": str(ObjectId()), **config, "created_at": get_current_datetime()}
        )

    else:

        await config_coll.replace_one(
            {},
            {
                **config,
                "created_at": get_current_datetime(),
            },
            upsert=True,
        )

    dataset_coll = db.get_collection(Collections.MODEL_DATASET)
    num_docs = await dataset_coll.count_documents({})

    if num_docs > 0:
        await dataset_coll.drop()

    await dataset_coll.insert_many(records)

    # first 10 records
    return records[:10]


async def convert_file_to_df(file: UploadFile) -> pd.DataFrame:
    file_extension = file.filename.split(".")[-1]
    if file_extension.lower() == "csv":
        return pd.read_csv(file.file, keep_default_na=False)
    elif file_extension.lower() == "json":
        default = "lines"
        file.file.seek(0)
        first_char = await file.read(1)
        file.file.seek(0)
        if first_char == b"[":
            default = "array"

        if default == "lines":
            return pd.read_json(file.file, lines=True)
        else:
            # print(file.file, type(file.file))
            data = json.load(file.file)
            return pd.DataFrame(data)

    raise Exception(f"Invalid file")


# def translate_text(text, target_language='vi'):
#     translator = Translator()
#     translator.raise_Exception = True
#     if not text:
#         return ""
#     translated_text = translator.translate(text, dest=target_language)
#     return translated_text.text
# df = get_datasets_from_csa_be(client)
# df = preprocess_datasets(df, ["title", "pos_rw", "neg_rw"])


# def get_phobert_tokenizer_config() -> dict:
#     # ["<s>": 0 -> [CLS], "</s>": 2, "<unk>": 3, "<pad>": 1, "<mask>": 64000]
#     special_tokens = tokenizer.all_special_tokens
#     special_ids = tokenizer.all_special_ids

#     return {token: id for token, id in zip(special_tokens, special_ids)}
