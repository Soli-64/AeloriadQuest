import pygame
import json
from src.Utils.interface import Interface
import src.Utils.pygame_functions as f_pg

class Weapon(pygame.sprite.Sprite):

    x = 100
    y = 100

    def __init__(self, name: str, level: int, map_manager, player):
        super().__init__()
        self.name = name
        self.level = level
        self.map_manager = map_manager
        self.player = player
        self.position = [self.x, self.y]
        self.get_data()
        self.icon = Interface(self.map_manager.screen, [205, 368], self.item_image, [])

    def blit_inventory_image(self):
        self.icon.blit()

    def get_data(self):
        with open(f'./assets/json/weapons/{self.name}.json', 'r') as file:
            data = json.load(file)
            self.item_image = f_pg.pygame_image(data['item_image'], [100, 100])
            #self.game_image = pygame.image.load(data['game_image'])
            self.rarity = data['rarity']
            self.reach = data['reach']
            self.damage = data['level_stats'][str(self.level)]['damage']
            self.munition_type = data['munition_type']
            self.munitions = "infinite"

    def move(self):
        self.position[0] = self.player.position[0]
        self.position[1] = self.player.position[1]

    def attack(self):
        for enemy in self.map_manager.get_map().enemys:
            knock_stats = self.player.localize(enemy, self.player.reach + self.reach)
            if knock_stats:
                enemy.apply_damage(self.damage)

    def magic_attack(self): print('test')
    def fire_attack(self): print('test')
