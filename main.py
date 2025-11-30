
from game_app import GameApp
from game_service import GameService
from websocket_service import WebsocketServiceImpl
from config import server_url, screen_resolution_width, screen_resolution_height, screen_font_size

if "__main__" == __name__:

    websocket_service = WebsocketServiceImpl(server_url)

    game_service = GameService(screen_resolution_width, screen_resolution_height, screen_font_size, 30, websocket_service)

    app = GameApp(websocket_service, game_service)
    app.run()
