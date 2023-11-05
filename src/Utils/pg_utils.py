import pygame as pg, sys, src.Utils.colors as co

def pygame_image(_path, _d):
    image = pg.image.load(_path)
    image = pg.transform.scale(image, (_d[0], _d[1]))
    return image

def text(_text, _police, _size, _color=co.BLACK):
    font = pg.font.Font(_police, _size)
    return font.render(str(_text), True, _color)

def percent(_width, _percent):
    return (_width / 100) * _percent

def toHours(p): return (p * 60000) * 60

def ImageToSprite(image): return ImageSprite(image)

def ImagesSuperposition(size, image, other_image):
    final_image = pg.Surface(size)
    final_image.blit(image, (0, 0))
    final_image.blit(other_image, (0, 0))
    return final_image


class ImageSprite(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

    def rotate(self, degree):
        self.image = pg.transform.rotozoom(self.image, degree, 1)


class GameScene:

    def __init__(self, game):
        self.game = game
        self.clock = pg.time.Clock()

    def launch_loop(self, scene_script, handle_scene_events= lambda e: e):

        for element in self.game.ui_manager.get_root_container().elements:
            element.kill()

        while self.game.game_running:
            time_delta = self.clock.tick(60)

            scene_script(time_delta)

            pg.display.flip()

            for event in pg.event.get():

                self.game.handle_events(event)

                handle_scene_events(event)

        pg.quit()
        sys.exit()
