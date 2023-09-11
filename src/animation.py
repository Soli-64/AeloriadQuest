import pygame
import src.Utils.pg_utils as f_pg
from src.Utils.settings import *
from threading import Thread

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, _path):
        super().__init__()
        self.path = _path
        self.sprite_sheet = pygame.image.load(self.path)
        self.animation_index = 0
        self.clock = 0
        self.images = []
        self.speed = 3

    def set_spritesheets(self):
        self.sprite_sheet = pygame.image.load(self.path)
        self.sprite_damaged_sheet = 'default damaged sprite sheet'

    def set_enemy_animation(self, _path):
        self.sprite_damaged_sheet = pygame.image.load(f'{_path}')
        self.images['damaged'] = self.get_images_d(0)

    def animations(self, _name):
        self.image = self.images[_name][self.animation_index]
        self.image.set_colorkey(0, 0)
        self.clock += self.speed * 8

        if self.clock >= 170:

            self.animation_index += 1

            if self.animation_index >= len(self.images[_name]):
                self.animation_index = 0

            self.clock = 0

    def get_images_d(self, _y):
        images = []
        for i in range(0, 3):
            x = i * 32
            image = self.get_image_d(x, _y)
            images.append(image)
        return images

    def get_images(self, _y):
        images = []
        for i in range(0, 3):
            x = i*32
            image = self.get_image(x, _y)
            images.append(image)
        return images

    def get_splited_images(self, _file_path, _animation_name, _images_number):
        images = []
        for i in range(0, _images_number):
            image = f_pg.pygame_image(f'{_file_path}/{_animation_name}{i}.png', [64, 64])
            surface = pygame.Surface([64, 64])
            surface.blit(image, (0, 0))
            images.append(surface)
        return images

    def get_image_d(self, _x, _y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_damaged_sheet, (0, 0), (_x, _y, 32, 32))
        return image

    def get_image(self, _x, _y) -> pygame.Surface:
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (_x, _y, 32, 32))
        return image


class AnimateEffectSprite(pygame.sprite.Sprite):

    def __init__(self, file_path, animation_name, images_number, position):
        super().__init__()
        self.file_path = file_path
        self.animation_name = animation_name
        self.images_number = images_number
        self.map_manager = None
        self.animation_index = 0
        self.position = [position[0] + 30, position[1] + 15]
        self.clock = 0
        self.speed = 3

        self.set_none_image()

        self.rect = self.image.get_rect()
        self.images = self.get_splited_images()

    def set_none_image(self): self.image = f_pg.pygame_image('./assets/images/empty.png', [16, 16])

    def play_animation(self, map_manager, position):

        self.map_manager = map_manager
        self.position = position
        self.index = 0
        self.images_number = len(self.images)

        if self.map_manager.player.direction == 'up':
            self.rotate(90)
            self.rect.x = self.map_manager.player.rect.x + 7
            self.rect.y = self.map_manager.player.rect.y - 20
        elif self.map_manager.player.direction == 'right':
            self.rect.x = self.map_manager.player.rect.x + 25
            self.rect.y = self.map_manager.player.rect.y + 15
        elif self.map_manager.player.direction == 'left':
            self.rotate(180)
            self.rect.x = self.map_manager.player.rect.x - 13
            self.rect.y = self.map_manager.player.rect.y + 15
        elif self.map_manager.player.direction == 'down':
            self.rotate(270)
            self.rect.x = self.map_manager.player.rect.x + 5
            self.rect.y = self.map_manager.player.rect.y + 33
        else:
            print('erreur direction player')

        self.animation_timer = pygame.time.set_timer(SLASH_ANIMATION_TIMER, 50)

    def stop_animation(self):
        pygame.time.set_timer(SLASH_ANIMATION_TIMER, 0)
        self.set_none_image()

    def updated(self):
        self.rect.topleft = self.position
        self.image = self.images[self.animation_index]
        if self.map_manager.player.direction == 'up':
            self.rotate(90)
            self.rect.x = self.map_manager.player.rect.x + 7
            self.rect.y = self.map_manager.player.rect.y - 20
        elif self.map_manager.player.direction == 'right':
            self.rotate(0)
            self.rect.x = self.map_manager.player.rect.x + 25
            self.rect.y = self.map_manager.player.rect.y + 15
        elif self.map_manager.player.direction == 'left':
            self.rotate(180)
            self.rect.x = self.map_manager.player.rect.x - 13
            self.rect.y = self.map_manager.player.rect.y + 15
        elif self.map_manager.player.direction == 'down':
            self.rotate(270)
            self.rect.x = self.map_manager.player.rect.x + 5
            self.rect.y = self.map_manager.player.rect.y + 33
        self.animation_index += 1
        if self.animation_index >= self.images_number:
            self.animation_index = 0
            self.stop_animation()

    def handle_event(self, event):
        if event.type == SLASH_ANIMATION_TIMER:
            self.updated()

    def rotate(self, degree):
        self.image = pg.transform.rotozoom(self.image, degree, 1)

    def get_splited_images(self):
        images = []
        for i in range(0, self.images_number):
            image = f_pg.pygame_image(f'{self.file_path}/{self.animation_name}{i}.png', [16, 16])
            images.append(image)
        return images

"""
class EffectAnimator:

    def __init__(self, _file_path, _image_name, position):
        self.file_path = _file_path
        self.image_name = _image_name
        self.position = position
        self.isAnimating = False
        self.sprite = False
        self.map_manager = None
        self.index = 0
        self.clock = 0

    def remove_sprite(self):
        self.map_manager.get_map().effects.remove(self.sprite)
        self.map_manager.get_group().remove(self.sprite)
        self.sprite = False

    def next_image(self, max_index):
        if self.sprite:
            self.remove_sprite()

        self.image = f_pg.pygame_image(f'{self.file_path}/{self.image_name}{self.index}.png', [16, 16])
        self.sprite = f_pg.ImageToSprite(self.image)
        if self.map_manager.player.direction == 'up':
            self.sprite.rotate(90)
            self.sprite.rect.x = self.map_manager.player.rect.x + 7
            self.sprite.rect.y = self.map_manager.player.rect.y - 20
        elif self.map_manager.player.direction == 'right':
            self.sprite.rotate(0)
            self.sprite.rect.x = self.map_manager.player.rect.x + 25
            self.sprite.rect.y = self.map_manager.player.rect.y + 15
        elif self.map_manager.player.direction == 'left':
            self.sprite.rotate(180)
            self.sprite.rect.x = self.map_manager.player.rect.x - 13
            self.sprite.rect.y = self.map_manager.player.rect.y + 15
        elif self.map_manager.player.direction == 'down':
            self.sprite.rotate(270)
            self.sprite.rect.x = self.map_manager.player.rect.x + 5
            self.sprite.rect.y = self.map_manager.player.rect.y + 33
        else:
            print('erreur direction player')

        self.map_manager.get_map().effects.append(self.sprite)
        self.map_manager.get_group().add(self.sprite)

        self.index += 1
        if self.index >= max_index:
            animation = Thread(target=lambda:f_pg.time_event(self.remove_sprite, 90))
            animation.start()
            self.index = 0
            self.isAnimating = False
            for sprite in self.map_manager.get_group():
                if type(sprite) is EffectAnimator:
                    self.map_manager.get_group().remove(sprite)
                    self.map_manager.get_map().effects.remove(sprite)

    def launch_animation(self, position, map_manager):
        if self.isAnimating == False:
            self.isAnimating = True
            self.map_manager = map_manager
            self.position = [position[0] + 30, position[1] + 15]
            self.index = 0
            animation = Thread(target=lambda:f_pg.set_interval(lambda :self.next_image(3), 90, 3))
            animation.start()"""
