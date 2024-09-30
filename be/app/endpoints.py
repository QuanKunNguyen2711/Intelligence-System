# from typing_extensions import Annotated
# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from SystemManagement.enums import SystemRole
# from app.common.authentication import protected_route
# from app.common.db_connector import client
# from ModelAI.services import fine_tuning_model, infer_prediction
# from DataPipeline.services import (
#     get_datasets_from_csa_be,
#     preprocess_inputs_concurrently,
#     save_datasets_as_db_records,
# )
# import time
# import logging
# import pandas as pd
# import torch
# from app.common.repository import DatasetConfigRepository
# from app.schemas import InferenceSchema, ModelSchema, PreprocessSchema
# from app.utils import generate_model_id, get_current_datetime

# router = APIRouter()

# logging.basicConfig(
#     level=logging.INFO,
# )
# logger = logging.getLogger(__name__)

# # Dependencies
# AuthCredentialDepend = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]


# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


# @router.post("/train", status_code=200)
# @protected_route([SystemRole.DATASCIENTIST, SystemRole.ADMINISTRATOR])
# def train(
#     model_info: ModelSchema, CREDENTIALS: AuthCredentialDepend, CURRENT_USER=None
# ):
#     db_str, current_user_id = CURRENT_USER.get("db"), CURRENT_USER.get("_id")
#     model_info = model_info.model_dump()
#     name = model_info.get("name")
#     description = model_info.get("description")
#     dataset_obj_id = model_info.get("dataset_obj_id")
#     model_id_str = generate_model_id(name)

#     repo = DatasetConfigRepository(db_str)
#     df, cols = repo.get_dataset_from_db(dataset_obj_id)

#     df_small = df.iloc[: len(df)]

#     logger.info(f"{get_current_datetime()} - Start to fine-tune model")
#     model, evaluation_metric = fine_tuning_model(
#         df_small,
#         cols,
#         db_str=db_str,
#         hidden_size=model_info.get("hidden_size", 64),
#         batch_size=model_info.get("batch_size", 64),
#         num_epochs=model_info.get("num_epochs", 30),
#         model_id_str=model_id_str,
#         repo=repo,
#     )

#     logger.info(f"{get_current_datetime()} - Start to save model")
#     repo.save_model_db(
#         model,
#         dataset_obj_id=dataset_obj_id,
#         evaluation_metric=evaluation_metric,
#         model_name=name,
#         model_id_str=model_id_str,
#         model_description=description,
#     )




    


# @router.post("/predict", status_code=200)
# @protected_route([SystemRole.DATASCIENTIST, SystemRole.ADMINISTRATOR])
# def predict(
#     inference: InferenceSchema, CREDENTIALS: AuthCredentialDepend, CURRENT_USER=None
# ):
#     inference = inference.model_dump()
#     text = inference.get("text", "")
#     model_id = inference.get("model_id", "")
    
#     db_str, cur_user_id = CURRENT_USER.get("db"), CURRENT_USER.get("_id")
    
#     return {"score": infer_prediction(text, model_id, db_str)}
