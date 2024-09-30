import asyncio
from fastapi import APIRouter
import pandas as pd
from ModelAI.schemas import TrainModelSchema
from ModelAI.services import fine_tuning_model
from SystemManagement.enums import SystemRole
from app.common.authentication import protected_route
from app.common.db_collections import Collections
from app.common.dependencies import AuthCredentialDepend
from app.common.db_connector import client
import logging

from app.common.websocket import WebsocketEventResult

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/train", status_code=200)
@protected_route([SystemRole.DATA_SCIENTIST, SystemRole.HOTEL_OWNER])
async def train(
    model_info: TrainModelSchema, CREDENTIALS: AuthCredentialDepend, CURRENT_USER=None
):
    db_str, cur_user_id = CURRENT_USER.get("db"), CURRENT_USER.get("_id")
    model_info = model_info.model_dump()
    name = model_info.get("name")
    description = model_info.get("description")
    hidden_size = model_info.get("hidden_size")
    batch_size = model_info.get("batch_size")
    num_epochs = model_info.get("num_epochs")

    db = client.get_database(db_str)
    dataset_coll = db.get_collection(Collections.MODEL_DATASET)
    dataset = await dataset_coll.find({}).to_list(length=None)

    config_coll = db.get_collection(Collections.DATASET_CONFIG)
    config = await config_coll.find_one({})

    cols = config.get("features") + [config.get("label")]

    training_epoch_coll = db.get_collection(Collections.TRAINING_EPOCH)

    df = pd.DataFrame(dataset, columns=cols)

    task = asyncio.create_task(fine_tuning_model(
        df,
        cols,
        db_str=db_str,
        name=name,
        description=description,
        training_epoch_coll=training_epoch_coll,
        cur_user_id=cur_user_id,
        hidden_size=hidden_size,
        batch_size=batch_size,
        num_epochs=num_epochs,
    ))

    return {
        "message": "Fine-tuning task is running in background",
        "event": WebsocketEventResult.FINE_TUNING,
    }
