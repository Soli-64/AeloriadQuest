import pygame


def pygame_image(path, d):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (d[0], d[1]))
    return image