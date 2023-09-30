import pygame as pg
import src.Utils.colors as co

def pygame_image(_path, _d):
    image = pg.image.load(_path)
    image = pg.transform.scale(image, (_d[0], _d[1]))
    return image

def text(_text, _polic, _size, _color=co.BLACK):
    font = pg.font.Font(_polic, _size)
    return font.render(str(_text), True, _color)

def percent(_width, _percent):
    return (_width / 100) * _percent

def toHours(p): return (p * 60000) * 60

def set_interval(_event, _millis: int, loops: int) -> None:
    ticks = pg.time.get_ticks()
    index = -1
    func = _event
    running = True
    while running:
        if pg.time.get_ticks() >= ticks + _millis:
            if index >= loops - 1:
                running = False
                return True
            ticks = pg.time.get_ticks()
            func()
            index += 1
            print(index)

def time_event(_event, _millis: int) -> None:
    ticks = pg.time.get_ticks()
    func = _event
    running = True
    while running:
        if pg.time.get_ticks() == ticks + _millis:
            ticks = pg.time.get_ticks()
            func()
            running = False


def ImageToSprite(image): return ImageSprite(image)


class ImageSprite(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

    def rotate(self, degree):
        self.image = pg.transform.rotozoom(self.image, degree, 1)
