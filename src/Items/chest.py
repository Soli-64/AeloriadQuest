import pygame, random, src.Utils.pg_utils as f_pg, time
from src.Items.item import Item


class Chest(Item):

    def __init__(self, x, y, map_manager):
        super().__init__('chest', x, y, map_manager)
        self.map_manager = map_manager
        self.content = {
            'money': random.randint(100, 100),
            'xp': random.randint(50, 100),
            'weapons': []
        }

    def obtain(self):
        self.image = f_pg.pygame_image(f'./assets/images/items/chest-open.png', [16, 16])
        self.map_manager.player.add_money(self.content['money'])
        self.map_manager.get_map().items.remove(self)
        self.map_manager.get_map().group.remove(self)
