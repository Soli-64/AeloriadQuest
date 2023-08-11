import pygame as pg


def pygame_image(path, d):
    image = pg.image.load(path)
    image = pg.transform.scale(image, (d[0], d[1]))
    return image

def text(text, polic, size):
    font = pg.font.Font(polic, size)
    return font.render(str(text), True, (0, 0, 0))