import pygame
import json
from src.Elements.interface import Interface
import src.Utils.pg_utils as f_pg
from src.animation import AnimateSprite

class Weapon(AnimateSprite, pygame.sprite.Sprite):

    x = 100
    y = 100

    def __init__(self, name: str, level: int, map_manager, player, animation_path):
        super().__init__(animation_path)
        self.name = name
        self.level = level
        self.map_manager = map_manager
        self.player = player
        self.image = pygame.Surface([16, 16])
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
        self.position = [self.rect.x, self.rect.y]
        self.get_data()

        self.images = {
            'slash': self.get_splited_images('./assets/images/sprite/slash', 'slash_effect_anim_f', 2)
        }

        self.icon = Interface(self.map_manager.screen, [205, 368], self.item_image, [])

    def blit_inventory_image(self):
        self.icon.blit()

    def get_data(self):
        with open(f'./assets/json/weapons/{self.name}.json', 'r') as file:
            data = json.load(file)
            self.item_image = f_pg.pygame_image(data['item_image'], [100, 100])
            #self.game_image = pygame.image.load(data['game_image'])
            self.type = data['type']
            self.rarity = data['rarity']
            self.reach = data['reach']
            self.damage = data['level_stats'][str(self.level)]['damage']
            self.munition_type = data['munition_type']
            self.munitions = "infinite"

    def move(self):
        self.rect.topleft = self.position

    def attack(self):
        for enemy in self.map_manager.get_map().enemys:
            knock_stats = self.player.localize(enemy, self.player.reach + self.reach)
            if knock_stats:
                enemy.apply_damage(self.damage)
        for x in range(0, 2):
            self.animations('slash')

    def magic_attack(self): return
    def fire_attack(self): return
