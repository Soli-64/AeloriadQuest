import pygame
from src.Utils.pygame_functions import pygame_image

class Projectile(pygame.sprite.Sprite):

    def __init__(self, name, map_manager, player, x, y):
        super().__init__()
        self.image = pygame_image(f'./images/projectile/{name}.png', [20, 20])
        self.map_manager = map_manager
        self.player = player
        self.position = [x, y - 45]
        self.speed = 2

    def playerX(self): return self.player.position[0]

    def blit(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))

    def move(self):
        self.position[1] -= self.speed
        for enemy in self.map_manager.get_map().enemys:
            # supprimer le projectile
            self.remove()
            # infliger des dégats
            enemy.damage(self.player.damage)

    def remove(self):
        self.map_manager.get_map().projectiles.remove(self)
