from fastapi import WebSocket
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_payload(self, payload_json: str, websocket: WebSocket):
        await websocket.send_text(payload_json)

    async def broadcast(self, payload_json: str):
        for connection in self.active_connections:
            await connection.send_text(payload_json)