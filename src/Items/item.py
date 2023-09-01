import pygame
import src.Utils.pg_utils as f_pg
from src.entity import Entity

class Item(pygame.sprite.Sprite):

    def __init__(self, name, x, y, map_manager):
        super().__init__()
        self.name = name
        self.map_manager = map_manager
        self.image = f_pg.pygame_image(f'./assets/images/items/{self.name}.png', [16, 16])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

    def remove(self):
        self.map_manager.get_map().items.remove(self)
