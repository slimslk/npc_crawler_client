import pygame

from game_map import GameMap
from config import game_field_width, game_field_height, key_mapping, game_field_font_size


class GameScreen:
    def __init__(self, screen, font, player, game_map: GameMap):

        self.game_field_font_size = game_field_font_size
        self.screen = screen
        self.font = font
        self.player = player

        self.game_map = game_map

        self.is_finished = False

        self.display_map_width = game_field_width
        self.display_map_height = game_field_height
        self.player_coord = (self.display_map_width // 2, self.display_map_height // 2)
        self.actions = key_mapping

    def render_game_window(self):
        self.screen.fill((0, 0, 0))
        player_x, player_y = self.player.position
        # --- Top status line ---
        top_text = f"Player: {self.player.name} || Inventory: {'|'.join(self.player.inventory)}"
        top_surface = self.font.render(top_text, True, (255, 255, 255))
        self.screen.blit(top_surface, (0, 0))

        # --- Map rendering ---
        padding_x = 2  # horizontal padding between cells
        padding_y = 2  # vertical padding between cells
        cell_width = self.game_field_font_size + padding_x
        cell_height = self.game_field_font_size + padding_y
        map_width, map_height = self.game_map.get_map_size()

        # Start drawing map below top status line
        map_offset_y = top_surface.get_height() + 2  # extra 2 px space
        render_map_start_position_x = player_x - self.display_map_height // 2
        render_map_start_position_y = player_y - self.display_map_width // 2
        if render_map_start_position_x < 0:
            render_map_start_position_x = 0
        if render_map_start_position_y < 0:
            render_map_start_position_y = 0
        for y in range(self.display_map_width):
            if render_map_start_position_y + y > map_width - 1:
                break
            for x in range(self.display_map_height):
                try:
                    if render_map_start_position_x + x > map_height - 1:
                        break
                    rmp_x = render_map_start_position_x + x
                    rmp_y = render_map_start_position_y + y
                    char, color = self.game_map.get_map()[rmp_x][rmp_y]
                except IndexError:
                    print(x, y)
                    raise IndexError
                img = self.font.render(char, True, color)
                self.screen.blit(img, (y * cell_width, map_offset_y + x * cell_height))
            print()

        # --- Bottom stats line ---
        stats_text = (f"HP: {self.player.health}"
                      f" ST: {self.player.energy}"
                      f" SAT: {self.player.hungry}"
                      f" AM: {self.player.attack_modifier}"
                      f" AD: {self.player.attack_damage}"
                      f" DEF: {self.player.defence}")
        stats_surface = self.font.render(stats_text, True, (255, 255, 0))
        self.screen.blit(stats_surface, (0, map_offset_y + self.display_map_height * cell_height + 2))

        pygame.display.flip()

    def update_size(self, height, width):
        self.display_map_height = height
        self.display_map_width = width
