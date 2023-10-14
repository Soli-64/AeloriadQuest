import pygame
from src.Utils.settings import *


class Interface:

    def __init__(self, screen, pos, image, rects):
        self.screen = screen
        self.x = pos[0]
        self.y = pos[1]
        self.image = image
        self.rects = rects

    def blit(self):
        if self.image:
            self.screen.blit(self.image, (self.x, self.y))
        elif self.rects:
            for rect in self.rects:
                pass

class Cadre:
    def __init__(self, screen, color, rect, border_width):
        self.screen = screen
        self.color = color
        self.rect = rect
        self.border = border_width
    def blit(self): pygame.draw.rect(self.screen, self.color, self.rect, self.border)

class Alert:

    def __init__(self, game, text, color, seconds, pos):

        self.game = game

        self.text = text
        self.color = color
        self.time = int(seconds * 1000)
        self.pos = pos
        self.font = pygame.font.Font(None, 18) # pygame.font.Font('./assets/fonts/dialog_font.ttf', 21)

        surface = self.font.render(self.text, False, self.color)
        sprite = pygame.sprite.Sprite()
        sprite.image = surface
        sprite.rect = surface.get_rect()
        self.sprite = sprite
        self.sprite.feet = pygame.Rect(0, 0, self.sprite.rect.width * 0.5, 12)
        self.sprite.rect.x, self.sprite.rect.y = pos[0], pos[1]

        self.game.map_manager.get_map().effects.append( self.sprite )
        self.game.map_manager.get_group().add( self.sprite )

        self.game.alerts.append(self)

        pygame.time.set_timer(REMOVE_ALERTS, self.time)

    def end(self): self.game.map_manager.get_group().remove(self.sprite)
