import pygame


class Interface:

    def __init__(self, screen, x, y, image, rects):
        self.screen = screen
        self.x = x
        self.y = y
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

class Screen_Point:

    def __init__(self, x, y, element_size):
        self.x = x
        self.y = y
        self.size = element_size
