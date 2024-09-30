from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from app.common.authentication import get_user_by_token
from app.common.websocket import WebSocketManager, WebsocketEventResult
import os
from dotenv import load_dotenv
import warnings
from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging
import SystemManagement.endpoints
import DataPipeline.endpoints
import ModelAI.endpoints

from app.common.websocket import ws_manager

load_dotenv()

warnings.filterwarnings("ignore", category=FutureWarning, message="`resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`")

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    'http://localhost:3000',
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# async def add_task(websocket: WebSocket, task_id: str):
#     if websocket not in connections:
#         connections[websocket] = []
#     loop = asyncio.get_running_loop()
#     task = loop.run_in_executor(executor, blocking_task, task_id)
#     connections[websocket].append((task_id, task))
#     await notify_task_completion()

# async def notify_task_completion():
#     completed_tasks = []
#     for websocket, tasks in connections.items():
#         for task_id, task in tasks:
#             if task.done():
#                 result = task.result()
#                 completed_tasks.append((websocket, task_id, result))
    
#     for websocket, task_id, result in completed_tasks:
#         await websocket.send_text(f"Task finished: {result}")
#         connections[websocket] = [(tid, t) for tid, t in connections[websocket] if tid != task_id]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user = await get_user_by_token(token, {})
    user_id = user.get("_id")
    await ws_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_ws({"test": "heello", "event": WebsocketEventResult.PREPROCESS_DATASET})
            # await ws_manager.send_personal_message(f"You wrote: {data}", token)
            # await ws_manager.broadcast(f"Broadcast message from {token}: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(token)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url=os.environ.get("DOCS_ROUTE"))

# Include Routers
# app.include_router(endpoints.router, prefix="/api", tags=["Word Segmentation"])
app.include_router(SystemManagement.endpoints.router, prefix="/api", tags=["System Management"])
app.include_router(DataPipeline.endpoints.router, prefix="/api", tags=["Data Pipeline"])
app.include_router(ModelAI.endpoints.router, prefix="/api", tags=["Model AI"])