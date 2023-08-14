import pygame as pg
import src.Utils.colors as co

def pygame_image(path, d):
    image = pg.image.load(path)
    image = pg.transform.scale(image, (d[0], d[1]))
    return image

def text(text, polic, size, color=co.BLACK):
    font = pg.font.Font(polic, size)
    return font.render(str(text), True, color)

def percent(width, percent):
    return (width / 100) * percent
