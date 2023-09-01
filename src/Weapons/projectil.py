import pygame
import src.Utils.pg_utils as f_pg
from src.entity import Entity

class Projectil(pygame.sprite.Sprite):

    def __init__(self, map_manager):
        super().__init__()
        self.map_manager = map_manager
        self.image = f_pg.pygame_image('assets/images/weapons/projectile/projectile.png', [7, 7])
        self.rect = self.image.get_rect()
        x = self.map_manager.player.position[0]
        y = self.map_manager.player.position[1]
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

    def isEnemy(self): return False

    def remove(self):
        self.map_manager.get_map().projectils.remove(self)
        self.map_manager.get_group().remove(self)

    def move(self):
        self.position[1] -= 4
        for enemy in self.map_manager.check_projectile_collision(self, self.map_manager.get_map().enemys):
            self.remove()
            enemy.apply_damage(self.map_manager.player.selected_weapon.damage)

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom