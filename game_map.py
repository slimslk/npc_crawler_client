from game_objects import game_objects


class GameMap:
    def __init__(self):
        self.game_map = []

        self.player_coord = (0, 0)
        self.height = 25
        self.width = 80

    def generate_map(self, width, height):
        self.width = width
        self.height = height
        self.game_map = [[(".", (200, 200, 200)) for _ in range(self.width)] for _ in range(self.height)]

    def update_map(self, map_data: dict, player_name: str):
        for key, value in map_data.items():
            x, y = list(map(int, (key.split(",")))) #TODO Add check if key is not integer
            game_object = game_objects.get(value.upper(), value)
            if value.upper() not in game_objects.keys():
                if game_object == player_name:
                    game_object = ("@", (237, 201, 175))
                else:
                    game_object = ("e", (255, 165, 0))
            self.game_map[x][y] = game_object


    def update_map_size(self, height, width):
        self.height = height
        self.width = width
        self.game_map = [["." for _ in range(self.width)] for _ in range(self.height)]

    def set_map(self, game_map):
        self.game_map = game_map

    def get_map(self):
        return self.game_map

    def get_map_size(self):
        return self.width, self.height
