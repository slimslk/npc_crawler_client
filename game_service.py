import pygame

from game_map import GameMap
from game_screen import GameScreen
from login_screen import LoginScreen
from player import Player
from websocket_service import IWebsocketService
from config import game_field_width, game_field_height
import controller


class GameService:
    def __init__(self, width, height, font_size, fps, websocket_service: IWebsocketService):

        self.player = Player()
        self.game_map = GameMap()
        self.game_map.generate_map(game_field_width,
                                   game_field_height)

        self.width = width
        self.height = height
        self.font_size = font_size
        self.is_running = False
        self.fps = fps
        self.clock = pygame.time.Clock()

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ASCII Game Client")

        self.font = pygame.font.SysFont("Consolas", self.font_size)
        self.font.get_height()
        self.clock = pygame.time.Clock()

        self.login_screen = LoginScreen(self.screen, self.font)
        self.game_screen = GameScreen(self.screen, self.font, self.player, self.game_map)
        self.logged_in = False

        self.websocket_service = websocket_service

    def is_running(self):
        return self.is_running

    async def run_game(self):
        self.is_running = True
        login_data = None

        while self.is_running:
            # ------ Login screen ---------
            while not self.login_screen.finished:
                self.login_screen.draw()
                for event in pygame.event.get():
                    login_data = self.login_screen.handle_event(event)
                self.clock.tick(self.fps)

            if isinstance(login_data, dict):
                if set(login_data.keys()) == {"user_id", "password"}:
                    message = {"user_id": login_data["user_id"]}
                    await self.websocket_service.send_message(message)

            await self._receive_updates()

            #-------- Game Screen --------
            while not self.game_screen.is_finished:
                self.game_screen.render_game_window()
                for event in pygame.event.get():
                    action = controller.handle_event(event)
                    if action == "exit":
                        self.game_screen.is_finished = True
                        continue
                    if self.player.is_dead:
                        continue
                    if action and isinstance(action, dict):
                        message = {"user_id": login_data["user_id"]} | action
                        await self.websocket_service.send_message(message)

                await self._receive_updates()
                self.clock.tick(self.fps)

            self.is_running = False

        pygame.quit()

    async def _receive_updates(self):
        response: dict = await self.websocket_service.receive_message()
        if response:
            if response.get("game_updates"):
                self.update_game_state(response["game_updates"])
            if response.get("player_stats"):
                self.update_player_stats(response["player_stats"])
            if response.get("location_updates"):
                self.update_location(response["location_updates"])

    def update_player_stats(self, player_data):
        self.player.update(player_data)

    def update_location(self, location_updates):
        self.game_map.update_map(location_updates, self.player.name)

    def update_game_state(self, game_updates: dict):
        if game_updates.get("location_size") and game_updates.get("location_data"):
            height, width = game_updates["location_size"]
            self.game_map.update_map_size(height, width)
            self.game_map.update_map(game_updates["location_data"], self.player.name)
