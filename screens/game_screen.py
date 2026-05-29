import pygame

from core import controller
from core.context import AppContext
from core.game_map import GameMap
from screens.base_screen import BaseScreen
from core.config.config import game_field_width, game_field_height, key_mapping, game_field_font_size, screen_font_size

from screens.popup.popup_factory import PopupFactory
from screens.const.screen_constants import LOGOUT_SCREEN, CHARACTER_SCREEN


class GameScreen(BaseScreen):
    _UI_OFFSET = 5
    _SCREEN_FONT_COLOR = (91, 104, 121)

    def __init__(self, screen, font: pygame.font.Font, context: AppContext, player, game_map: GameMap):

        super().__init__(screen, font, context)
        self.context = context
        self.player = player
        self.game_map = game_map

        self.game_field_font_size = game_field_font_size

        self.display_map_width = game_field_width
        self.display_map_height = game_field_height
        self.player_coord = (self.display_map_width // 2, self.display_map_height // 2)
        self.actions = key_mapping
        self.is_created = False

        self.player.name = self.context.selected_character
        self.popup_manager = self.context.popup_manager

    def handle_event(self, event):
        if self.player.is_dead and not self.popup_manager.is_active():
            self.open_death_popup()

        if self.popup_manager.is_active():
            action = self.popup_manager.handle_event(event)
            if action:
                self.popup_manager.close()
                if action in (LOGOUT_SCREEN, CHARACTER_SCREEN):
                    return {"event": action}
        else:
            action = controller.handle_event(event)
        if action and isinstance(action, dict):
            if "inventory" == action.get("action"):
                self.open_inventory_popup()
            elif "exit" == action.get("action"):
                self.open_exit_game_popup()
            else:
                self.context.ws.send(action)

    def open_inventory_popup(self):
        inv_popup = PopupFactory.create("inventory", self.screen,
                                        font=self.font,
                                        inventory=self.player.inventory,
                                        text_color=self._SCREEN_FONT_COLOR)
        self.popup_manager.open(inv_popup)

    def open_death_popup(self):
        popup_dead = PopupFactory.create("dead", self.screen, font=self.font)
        self.popup_manager.open(popup_dead)

    def open_exit_game_popup(self):
        popup_exit = PopupFactory.create("exit", self.screen, font=self.font)
        self.popup_manager.open(popup_exit)

    def draw(self):
        self.screen.fill((0, 0, 0))
        px, py = self.player.position

        # --- Top status line ---
        top_text = f"Player: {self.player.name}"
        top_surface = self.font.render(top_text, True, self._SCREEN_FONT_COLOR)
        self.screen.blit(top_surface, (screen_font_size, 5))

        # --- Game map ---
        map_w, map_h = self.game_map.get_map_size()
        ui_height_offset = top_surface.get_height() + self._UI_OFFSET

        padding = game_field_font_size // 1.5
        cell_w = self.game_field_font_size + padding
        cell_h = self.game_field_font_size + padding

        if map_w <= self.display_map_height:
            cam_x = 0
            render_w = map_w
            screen_offset_x = (self.display_map_height - map_w) * cell_w // 2
        else:
            cam_x = px - (self.display_map_height // 2)
            cam_x = max(0, min(cam_x, map_w - self.display_map_height))
            render_w = self.display_map_height
            screen_offset_x = 0

        if map_h <= self.display_map_width:
            cam_y = 0
            render_h = map_h
            screen_offset_y = 0
        else:
            cam_y = py - (self.display_map_width // 2)
            cam_y = max(0, min(cam_y, map_h - self.display_map_width))
            render_h = self.display_map_width
            screen_offset_y = 0

        grid = self.game_map.get_map()

        for s_x in range(render_w):
            for s_y in range(render_h):
                m_x = cam_x + s_x
                m_y = cam_y + s_y

                if 0 <= m_x < map_w and 0 <= m_y < map_h:
                    try:
                        char, color = grid[m_x][m_y]
                        img = self.font.render(char, True, color)

                        draw_x = ui_height_offset + screen_offset_x + (s_x * cell_w)
                        draw_y = ui_height_offset + screen_offset_y + (s_y * cell_h)
                        self.screen.blit(img, (draw_y, draw_x))
                    except IndexError:
                        continue

        # --- Bottom stats line ---
        stats_text = (f"HP: {self.player.health}"
                      f" ST: {self.player.energy}"
                      f" AM: {self.player.attack_modifier}"
                      f" AD: {self.player.attack_damage}"
                      f" DEF: {self.player.defence}"
                      f" SAT: {self.get_hunger_state_message(self.player.hungry)}")
        stats_surface = self.font.render(stats_text, True, self._SCREEN_FONT_COLOR)
        self.screen.blit(stats_surface, (0, top_surface.get_height() + self._UI_OFFSET * 2 +
                                         self.display_map_height * (self.game_field_font_size + padding)))
        message_test = f"{self.player.messages[-1]}"
        message_surface = self.font.render(message_test, True, self._SCREEN_FONT_COLOR)
        self.screen.blit(message_surface, (0, top_surface.get_height() + self._UI_OFFSET * 2 +
                                           self.display_map_height * (self.game_field_font_size + padding) +
                                           stats_surface.get_height()))

        self.popup_manager.draw()

        pygame.display.flip()

    def update_size(self, height, width):
        self.display_map_height = height
        self.display_map_width = width

    def get_hunger_state_message(self, state):
        state_message = {
            100: "Sated",
            80: "Hollow",
            50: "Gnawing",
            25: "Famished",
            10: "Ravenous",
            0: "Dying",
        }
        return state_message.get(state, "Starving")
