import pygame
#from src.Enemy.enemy import Enemy
from src.animation import AnimateSprite


class Entity(AnimateSprite):
    def __init__(self, name: str, path, x: int, y: int):
        super().__init__(path)

        self.image_path = path
        print(self.image_path)
        self.images = {
            'down': self.get_images(self.image_path, 0),
            'left': self.get_images(self.image_path, 32),
            'right': self.get_images(self.image_path, 64),
            'up': self.get_images(self.image_path, 96),
            'slash': self.get_splited_images('./assets/images/sprite/slash', 'slash_effect_anim_f', 2)
        }
        self.effects_images = {
            'damaged_down': self.get_images('./assets/images/sprite/effects/damaged.png', 0),
            'damaged_left': self.get_images('./assets/images/sprite/effects/damaged.png', 32),
            'damaged_right': self.get_images('./assets/images/sprite/effects/damaged.png', 64),
            'damaged_up': self.get_images('./assets/images/sprite/effects/damaged.png', 96),
        }

        self.name = name
        self.direction = 'down'
        self.sprite_sheet = pygame.image.load(path)
        self.image = self.get_image(self.image_path, 0, 0)
        self.image.set_colorkey(0, 0)
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

        self.position = [x, y]
        self.old_position = self.position.copy()

        self.speed = 3

    def localize_x(self, point, dist: int):
        if self.rect.x - point.rect.x <= dist and self.rect.x - point.rect.x >= 0:
            return True
        elif self.rect.x + dist >= point.rect.x and self.rect.x <= point.rect.x:
            return True
        else:
            return False

    def localize_y(self, point, dist: int):
        if self.rect.y - point.rect.y <= dist and self.rect.y - point.rect.y >= 0:
            return True
        elif self.rect.y + dist >= point.rect.y and self.rect.y <= point.rect.y:
            return True
        else:
            return False

    def localize(self, point, dist):
        if self.localize_x(point, dist) and self.localize_y(point, dist):
            return True
        else: return False

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self):
        self.animations('right')
        self.direction = 'right'
        self.position[0] += self.speed

    def move_left(self):
        self.animations('left')
        self.direction = 'left'
        self.position[0] -= self.speed

    def move_up(self):
        self.animations('up')
        self.direction = 'up'
        self.position[1] -= self.speed

    def move_down(self):
        self.animations('down')
        self.direction = 'down'
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