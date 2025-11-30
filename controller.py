import pygame
from config import key_mapping

keys = key_mapping


def handle_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "exit"
        action = keys.get(event.unicode, None)
        return action
