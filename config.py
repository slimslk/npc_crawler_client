import json

with open("config_dev.json", "r") as config:
    config = json.load(config)

server_url = config["server_url"]
display_settings = config["display_settings"]

screen_resolution_width = display_settings.get("screen_resolution_width")
screen_resolution_height = display_settings.get("screen_resolution_height")
screen_font_size = display_settings.get("screen_font_size")

game_field_width = display_settings.get("game_field_width")
game_field_height = display_settings.get("game_field_height")
game_field_font_size = display_settings.get("game_field_font_size")

key_mapping = config["key_mapping"]
