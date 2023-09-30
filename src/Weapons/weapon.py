import pygame
import json
from src.Elements.interface import Interface
import src.Utils.pg_utils as f_pg
from src.animation import AnimateSprite

class Weapon:

    x = 100
    y = 100

    def __init__(self, name: str, level: int, map_manager):
        self.name = name
        self.level = level
        self.map_manager = map_manager
        self.image = pygame.Surface([16, 16])
        self.get_data()

    def get_data(self):
        with open(f'./assets/json/items/weapons/{self.name}.json', 'r') as file:
            data = json.load(file)
            self.item_image = f_pg.pygame_image(data['item_image'], [100, 100])
            self.type = data['type']
            self.rarity = data['rarity']
            self.reach = data['reach']
            self.damage = data['level_stats'][str(self.level)]['damage']
            self.munition_type = data['munition_type']
            self.munitions = "infinite"

    def attack(self, player):
        for enemy in self.map_manager.get_map().enemys:
            knock_stats = player.localize(enemy, player.reach + self.reach)
            if knock_stats:
                enemy.apply_damage(self.damage)

    def magic_attack(self): return
    def fire_attack(self): return
