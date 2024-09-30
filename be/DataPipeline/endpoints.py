import asyncio
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile, concurrency
from DataPipeline.schemas import InferSchema
from DataPipeline.services import convert_file_to_df, preprocess_dataset
from ModelAI.services import infer_prediction
from SystemManagement.enums import SystemRole
from app.common.authentication import protected_route
from app.common.db_collections import Collections
from app.common.dependencies import AuthCredentialDepend
import json
import logging
from app.common.websocket import WebsocketEventResult
from app.common.db_connector import client

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/preprocess-dataset", status_code=200)
@protected_route([SystemRole.HOTEL_OWNER, SystemRole.DATA_SCIENTIST])
async def preprocess(
    CREDENTIALS: AuthCredentialDepend,
    mapping: str = Form(),
    file: UploadFile = File(...),
    CURRENT_USER=None,
):
    try:
        mapping = json.loads(mapping)
        if isinstance(mapping, str):
            mapping = json.loads(mapping)
            
        db_str, cur_user_id = CURRENT_USER.get("db"), CURRENT_USER.get("_id")

        features = mapping.get("features")
        label = mapping.get("label")
        
        df = await convert_file_to_df(file)
        # task = asyncio.create_task(preprocess_dataset(df, features, label, db_str, cur_user_id))
        
        # Registering the thread with background tasks to ensure FastAPI is aware of it
        # cols = features + [label]
        # preprocess_dataset(file, features, label, db_str)
        return await preprocess_dataset(df, features, label, db_str, cur_user_id)
        # return {"message": "Preprocessed task is running in background", "event": WebsocketEventResult.PREPROCESS_DATASET}

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        if isinstance(e, Exception):
            raise HTTPException(400, str(e))
        

@router.post("/infer", status_code=200)
@protected_route([SystemRole.HOTEL_OWNER, SystemRole.DATA_SCIENTIST])
async def infer(
    text: InferSchema, CREDENTIALS: AuthCredentialDepend, CURRENT_USER=None
):
    db_str, cur_user_id = CURRENT_USER.get("db"), CURRENT_USER.get("_id")
    db = client.get_database(db_str)
    model_coll = db.get_collection(Collections.SENTIMENT_MODEL)
    model = await model_coll.find_one()
    model_id = model.get("model_id")
    text = text.model_dump()
    
    return {"score": infer_prediction(text.get("text"), model_id, db_str)}
