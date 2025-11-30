import asyncio
import websockets
import json


class NetworkClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.server_url)

    async def send(self, data: dict):
        if self.websocket:
            await self.websocket.send(json.dumps(data))

    async def receive(self):
        if not self.websocket:
            return None

        try:
            msg = await asyncio.wait_for(self.websocket.recv(), timeout=0.05)
            return json.loads(msg)
        except asyncio.TimeoutError:
            return None

    async def close(self):
        if self.websocket:
            await self.websocket.close()
