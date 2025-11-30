class Player:
    def __init__(self, user_id="Unknown",
                 name="Void",
                 health=100,
                 energy=100,
                 hungry=100,
                 position=(0, 0),
                 direction=(0, 1),
                 map_id="None",
                 attack_modifier=0,
                 attack_damage=4,
                 defence=0
                 ):
        self.user_id = user_id
        self.name = name
        self.health = health
        self.energy = energy
        self.hungry = hungry
        self.position = position
        self.direction = direction
        self.inventory = []
        self.map_id = map_id
        self.attack_modifier = attack_modifier
        self.attack_damage = attack_damage
        self.defence = defence,
        self.is_dead = False

    def update(self, player_stats: dict):
        user_id = player_stats.get("id")
        if user_id is not None:
            self.user_id = user_id
        name = player_stats.get("name")
        if name is not None:
            self.name = name
        health = player_stats.get("health")
        if health is not None:
            self.health = health
        energy = player_stats.get("energy")
        if energy is not None:
            self.energy = energy
        hungry = player_stats.get("hungry")
        if hungry is not None:
            self.hungry = hungry
        position = player_stats.get("position")
        if position is not None:
            self.position = position
        direction = player_stats.get("direction")
        if direction is not None:
            self.direction = direction
        inventory = player_stats.get("inventory")
        if inventory is not None:
            self.inventory = inventory
        map_id = player_stats.get("map_id")
        if map_id is not None:
            self.map_id = map_id
        is_dead = player_stats.get("is_dead")
        if is_dead is not None:
            self.is_dead = is_dead
        attack_modifier = player_stats.get("attack_modifier")
        if attack_modifier is not None:
            self.attack_modifier = attack_modifier
        attack_damage = player_stats.get("attack_damage")
        if attack_damage is not None:
            self.attack_damage = attack_damage
        defence = player_stats.get("defence")
        if defence is not None:
            self.defence = defence
