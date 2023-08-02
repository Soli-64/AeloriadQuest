import pygame


class InanimateObject(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.object_img = pygame.image.load(f'../sprite/{name}.png')
        self.image = self.get_image(16, 48)

    def get_image(self, x, y):
        image = pygame.Surface([16, 16])
        image.blit(self.object_img, (0, 0), (x, y, 16, 16))
        return image


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.sprite_sheet = pygame.image.load(f'./sprite/{self.name}.png')
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'up': self.get_images(96)
        }
        self.speed = 3

    def set_enemy_animation(self):
        self.sprite_damaged_sheet = pygame.image.load(f'./sprite/enemys/damaged/{self.name}_d.png')
        self.images['damaged'] = self.get_images_d(0)

    def animations(self, name):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey(0, 0)
        self.clock += self.speed * 8

        if self.clock >= 170:

            self.animation_index += 1  # image suivante

            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0

            self.clock = 0

    def get_images_d(self, y):
        images = []
        for i in range(0, 3):
            x = i * 32
            image = self.get_image_d(x, y)
            images.append(image)
        return images

    def get_images(self, y):
        images = []
        for i in range(0, 3):
            x = i*32
            image = self.get_image(x, y)
            images.append(image)
        return images

    def get_image_d(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_damaged_sheet, (0, 0), (x, y, 32, 32))
        return image

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

