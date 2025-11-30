from abc import ABC, abstractmethod
from ws_client import NetworkClient


class IWebsocketService(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def send_message(self, message):
        pass

    @abstractmethod
    async def receive_message(self):
        pass

    @abstractmethod
    async def close_connection(self):
        pass


class WebsocketServiceImpl(IWebsocketService):
    def __init__(self, server_url):
        self.server_url = server_url
        self.network_client = NetworkClient(self.server_url)
        self.logged_in = False

    async def connect(self):
        await self.network_client.connect()

    async def send_message(self, message):
        await self.network_client.send(message)

    async def receive_message(self):
        return await self.network_client.receive()

    async def close_connection(self):
        await self.network_client.close()
