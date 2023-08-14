import pygame
#from src.Enemy.enemy import Enemy
from src.animation import AnimateSprite

class Entity(AnimateSprite):
    def __init__(self, name: str, path, x: int, y: int):
        super().__init__(path)
        self.image_path = path
        self.name = name
        self.sprite_sheet = pygame.image.load(path)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey(0, 0)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.speed = 3

    def localizeX(self, point, dist: int):
        if self.rect.x - point.rect.x <= dist and self.rect.x - point.rect.x >= 0:
            return True
        elif self.rect.x + dist >= point.rect.x and self.rect.x <= point.rect.x:
            return True
        else:
            return False

    def localizeY(self, point, dist: int):
        if self.rect.y - point.rect.y <= dist and self.rect.y - point.rect.y >= 0:
            return True
        elif self.rect.y + dist >= point.rect.y and self.rect.y <= point.rect.y:
            return True
        else:
            return False

    def localize(self, point, dist):
        if self.localizeX(point, dist) and self.localizeY(point, dist):
            return True
        else: return False

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self):
        self.animations('right')
        self.position[0] += self.speed

    def move_left(self):
        self.animations('left')
        self.position[0] -= self.speed

    def move_up(self):
        self.animations('up')
        self.position[1] -= self.speed

    def move_down(self):
        self.animations('down')
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        if self.isEnemy():
            self.modifyDirection()