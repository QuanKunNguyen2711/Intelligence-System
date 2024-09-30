# import os
# from typing import Union
# from bson import ObjectId
# from fastapi import HTTPException
# import pandas as pd
# import torch
# from app.common.db_connector import client
# from enum import Enum
# import logging

# from app.utils import generate_model_id, get_current_datetime

# logging.basicConfig(
#     level=logging.INFO,
# )
# logger = logging.getLogger(__name__)

# class DatasetConfigModel(str, Enum):
#     OBJ_ID_STR = "dataset_obj_id_str"
#     FEATURES = "features"
#     LABEL = "label"
    
# class RecordMetadata(str, Enum):
#     ID = "_id"
#     CREATED_AT = "created_at"
#     MODIFIED_AT = "modified_at"
#     CREATED_BY = "created_by"
#     MODIFIED_BY = "modified_by"
#     OBJECT_ID = "object_id"

# class DatasetConfigRepository:
#     def __init__(self, db_str: str, coll: str = DBCollections.DATASET_AI.value):
#         self.db_str = db_str
#         self.db = client.get_database(db_str)
#         self.repo = self.db.get_collection(coll)
        
#     def get_dataset_config(self, config_id: str):
#         return self.repo.find_one({"_id": config_id})
    
#     def get_dataset_from_db(self, config_id: str) -> Union[pd.DataFrame, list]:
#         config_detail = self.get_dataset_config(config_id)
#         if not config_detail:
#             raise HTTPException(400, f"Not found DatasetAI _id {config_id}")
        
#         obj_id_str = config_detail.get(DatasetConfigModel.OBJ_ID_STR.value)
        
#         # Projection features + label
#         features = config_detail.get(DatasetConfigModel.FEATURES.value)
#         label = config_detail.get(DatasetConfigModel.LABEL.value)
        
#         metadata_values = list(RecordMetadata.__members__.values())
        
#         records_obj = self.db.get_collection(obj_id_str).find({}, {v: 0 for v in metadata_values})
#         if not records_obj:
#             return []
        
#         records_obj = list(records_obj)
#         df = pd.DataFrame(records_obj, columns=features+[label])
        
#         return df, features+[label]
    
#     def save_epoch(self, model_id_str: str, epoch_num, train_loss, val_loss, done_at):
#         db = client.get_database(self.db_str)
#         epoch_col = db.get_collection(DBCollections.TRAINING_EPOCH)
        
#         epoch = {
#             "_id": str(ObjectId()),
#             "epoch_num": epoch_num,
#             "model_id_str": model_id_str,
#             "train_loss": train_loss,
#             "val_loss": val_loss,
#             "done_at": done_at
#         }
        
#         epoch_col.insert_one(epoch)
        
    
#     def save_model_db(
#         self, model, evaluation_metric: dict, dataset_obj_id: str, model_name: str, model_id_str: str, model_description: str
#     ):
#         save_dir = f"/app/csa_ai/models/{self.db_str}"
#         os.makedirs(save_dir, exist_ok=True)
        
#         torch.save(model, os.path.join(save_dir, f"{model_id_str}.pth"))

#         db = client.get_database(self.db_str)
#         model_col = db.get_collection(DBCollections.SENTIMENT_MODEL)

#         model_document = {
#             "_id": str(ObjectId()),
#             "name": model_name,
#             "description": model_description,
#             "model_id": model_id_str,
#             "dataset_obj_id": dataset_obj_id,
#             **evaluation_metric,
#             "created_at": get_current_datetime()
#         }
#         model_col.insert_one(model_document)
