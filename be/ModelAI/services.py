import asyncio
import os
import time
from typing import List
from bson import ObjectId
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    confusion_matrix,
)
from transformers import RobertaModel
import logging
import torch.nn as nn
import torch
import pandas as pd
from DataPipeline.services import get_train_val_test_dataloader
import torch.cuda

# from app.common.repository import DatasetConfigRepository
from transformers import AutoTokenizer
from app.common.db_collections import Collections
from app.common.db_connector import client
from app.common.utils import generate_model_id, get_current_datetime
from app.common.websocket import WebsocketEventResult, ws_manager

torch.cuda.empty_cache()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalysisModel(nn.Module):
    def __init__(self, num_classes: int, hidden_size: int = 64):
        super(SentimentAnalysisModel, self).__init__()
        self.phobert = RobertaModel.from_pretrained("vinai/phobert-base-v2")
        self.fc = nn.Linear(self.phobert.config.hidden_size, hidden_size)
        self.output = nn.Linear(hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        phobert_outputs = self.phobert(
            input_ids=input_ids, attention_mask=attention_mask
        )
        first_cls_token = phobert_outputs[0][:, 0, :]
        hidden = torch.relu(self.fc(first_cls_token))
        output = self.output(hidden)
        return output


class EarlyStopping:
    def __init__(self, tolerance=5, min_delta=0.0001):
        self.tolerance = tolerance
        self.min_delta = min_delta
        self.counter = 0
        self.best_val_loss = float("inf")
        self.early_stop = False

    def __call__(self, val_loss):
        if self.best_val_loss - val_loss > self.min_delta:
            self.best_val_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.tolerance:
                self.early_stop = True


class CheckpointSaver:
    def __init__(self, db_str: str):
        save_dir = f"/app/travel_booking_agencies/be/checkpoints/{db_str}"
        os.makedirs(save_dir, exist_ok=True)
        self.save_path = save_dir
        self.best_val_loss = float("inf")

    def save_checkpoint(self, model, val_loss):
        if val_loss < self.best_val_loss:
            self.best_val_loss = val_loss
            torch.save(
                model.state_dict(), os.path.join(self.save_path, "best_model.pth")
            )

    def load_best_model(self, model):
        model.load_state_dict(torch.load(self.save_path))
        return model


async def fine_tuning_model(
    df: pd.DataFrame,
    cols: List[str],
    training_epoch_coll,
    name: str,
    description: str,
    db_str: str,
    cur_user_id: str,
    hidden_size: int = 64,
    batch_size: int = 64,
    num_epochs: int = 100,
):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    if torch.cuda.is_available():
        logger.info(f"CUDA is available. GPU device count: {torch.cuda.device_count()}")
        logger.info(f"GPU device name: {torch.cuda.get_device_name(0)}")
    else:
        logger.info("CUDA is not available.")

    num_classes = len(df[cols[-1]].unique())
    label_min = df[cols[-1]].min()
    # Transform output of classification model from 0 to (N-C, C: num classes)
    if label_min == 1:
        df[cols[-1]] = df[cols[-1]] - 1

    model = SentimentAnalysisModel(num_classes=num_classes, hidden_size=hidden_size).to(
        device
    )
    logger.info(str(model))

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    # Early stopping, checkpoint saver
    early_stopping = EarlyStopping(tolerance=3, min_delta=0.0001)
    checkpoint_saver = CheckpointSaver(db_str=db_str)

    logger.info(f"{get_current_datetime()} - Start get train, val, test dataloader")
    train_loader, val_loader, test_loader = get_train_val_test_dataloader(
        df, cols, batch_size
    )

    for epoch in range(num_epochs):
        logger.info(f"{get_current_datetime()} - Start epoch {epoch+1}")
        loop = asyncio.get_event_loop()
        train_loss = await loop.run_in_executor(
            None, train_model, model, train_loader, optimizer, loss_fn, device
        )
        val_loss = await loop.run_in_executor(
            None, validate_model, model, val_loader, loss_fn, device
        )
        logger.info(
            f"{get_current_datetime()} - Epoch {epoch+1}/{num_epochs}, Training Loss: {train_loss}, Validation Loss: {val_loss}"
        )
        epoch_info = {
            "epoch": f"{epoch+1}/{num_epochs}",
            "train_loss": train_loss,
            "val_loss": val_loss,
            "created_at": get_current_datetime(),
        }

        await ws_manager.send_ws(
            {**epoch_info, "event": WebsocketEventResult.TRAINING_EPOCH},
            cur_user_id,
        )

        epoch_info.update({"_id": str(ObjectId())})

        await training_epoch_coll.insert_one(epoch_info)

        checkpoint_saver.save_checkpoint(model, val_loss)
        early_stopping(val_loss)

        if early_stopping.early_stop:
            logger.info(
                f"{get_current_datetime()} - Early stopping at {epoch+1}/{num_epochs}"
            )
            await ws_manager.send_ws(
                {
                    "early_stopping": f"{get_current_datetime()} - Early stopping at {epoch+1}/{num_epochs}",
                    "event": WebsocketEventResult.EARLY_STOPPING,
                },
                cur_user_id,
            )
            break

    # Perform testing model
    logger.info(f"{get_current_datetime()} - Start model testing")
    all_preds, all_labels = await loop.run_in_executor(
        None, test_model, model, test_loader, device
    )
    # all_preds, all_labels = test_model(model, test_loader, device)

    precision = precision_score(all_labels, all_preds, average="weighted")
    recall = recall_score(all_labels, all_preds, average="weighted")
    f1 = f1_score(all_labels, all_preds, average="weighted")
    accuracy = accuracy_score(all_labels, all_preds)
    conf_matrix = confusion_matrix(all_labels, all_preds)

    evaluation_metric = {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "accuracy": accuracy,
        "confusion_matrix": conf_matrix.tolist(),
    }

    logger.info(
        f"{get_current_datetime()} - Precision: {precision}, Recall: {recall}, F1-score: {f1}, Accuracy: {accuracy}, Confusion matrix: {conf_matrix.tolist()}",
    )

    await ws_manager.send_ws(
        {**evaluation_metric, "event": WebsocketEventResult.EVALUATION_METRIC},
        cur_user_id,
    )

    logger.info(f"{get_current_datetime()} - Start to save model")
    await save_model_db(
        model,
        evaluation_metric=evaluation_metric,
        db_str=db_str,
        model_name=name,
        model_description=description,
    )

    return evaluation_metric


def train_model(model, train_loader, optimizer, loss_fn, device):
    model.train()
    train_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()

        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        outputs = model(input_ids, attention_mask)
        loss = loss_fn(outputs, labels)
        train_loss += loss.item()

        loss.backward()
        optimizer.step()

    train_loss /= len(train_loader)
    return train_loss


def validate_model(model, val_loader, loss_fn, device):
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(input_ids, attention_mask)
            val_loss += loss_fn(outputs, labels).item()

    val_loss /= len(val_loader)
    return val_loss


def test_model(model, test_loader, device):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(input_ids, attention_mask)
            _, preds = torch.max(outputs, 1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    return all_preds, all_labels


def infer_prediction(text: str, model_id: str, db_str: str):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    if torch.cuda.is_available():
        logger.info(f"CUDA is available. GPU device count: {torch.cuda.device_count()}")
        logger.info(f"GPU device name: {torch.cuda.get_device_name(0)}")
    else:
        logger.info("CUDA is not available.")

    model = torch.load(
        f"/app/travel_booking_agencies/be/models/{db_str}/{model_id}.pth"
    ).to(device)

    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
    encoding = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=256,
        padding="max_length",
        return_attention_mask=True,
        truncation=True,
        return_token_type_ids=False,
        return_tensors="pt",
    )
    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        prob = torch.softmax(outputs, dim=1)
        predicted_class = torch.argmax(prob, dim=1).item()
        return predicted_class + 1


async def save_model_db(
    model,
    evaluation_metric: dict,
    db_str: str,
    model_name: str,
    model_description: str,
):
    save_dir = f"/app/travel_booking_agencies/be/models/{db_str}"
    os.makedirs(save_dir, exist_ok=True)

    model_id_str = generate_model_id(model_name)

    torch.save(model, os.path.join(save_dir, f"{model_id_str}.pth"))

    db = client.get_database(db_str)
    model_col = db.get_collection(Collections.SENTIMENT_MODEL)
    if await model_col.count_documents({}) > 0:
        await model_col.insert_one(
            {
                "_id": str(ObjectId()),
                "name": model_name,
                "description": model_description,
                "model_id": model_id_str,
                **evaluation_metric,
                "created_at": get_current_datetime(),
            }
        )

    else:
        await model_col.replace_one(
            {},
            {
                "name": model_name,
                "description": model_description,
                "model_id": model_id_str,
                **evaluation_metric,
                "created_at": get_current_datetime(),
            },
            upsert=True,
        )
