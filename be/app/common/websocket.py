from enum import Enum
from typing import Dict
from fastapi import WebSocket

class WebsocketEventResult(str, Enum):
    FILE_UPLOAD = 'file_upload'
    PREPROCESS_DATASET = 'preprocess_dataset'
    FINE_TUNING = 'fine_tuining'
    TRAINING_EPOCH = 'training_epoch'
    EARLY_STOPPING = 'early_stopping'
    EVALUATION_METRIC = 'evaluation_metric'

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_ws(self, message: dict, user_id: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)

    # async def broadcast(self, message: str):
    #     for connection in self.active_connections.values():
    #         await connection.send_text(message)
    
ws_manager = WebSocketManager()