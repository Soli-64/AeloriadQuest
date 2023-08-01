import pygame


class Weapon(pygame.sprite.Sprite):

    x = 100
    y = 100

    def __init__(self, name, level, map_manager, player):
        super().__init__()
        self.name = name
        self.item_image = pygame.image.load(f'./elements/weapons/item/{self.name}.png')
        self.game_image = pygame.image.load(f'./elements/weapons/game/{self.name}.png')
        self.level = level
        self.map_manager = map_manager
        self.player = player
        self.position = [self.x, self.y]

    def move(self):
        self.position[0] = self.player.position[0]
        self.position[1] = self.player.position[1]
