import asyncio

from game_service import GameService
from websocket_service import IWebsocketService


class GameApp:
    def __init__(self,
                 websocket_service: IWebsocketService,
                 game_service: GameService):

        self.websocket_service = websocket_service
        self.game_service = game_service

    async def start(self):
        await self.websocket_service.connect()
        await self.game_service.run_game()

        await self.websocket_service.close_connection()

    def run(self):
        asyncio.run(self.start())
