import pygame


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

    def __init__(self, game, text, color, time):
        self.game = game
        self.text = text
        self.color = color
        self.time = time
        self.font = pygame.font.Font('./assets/fonts/dialog_font.ttf', 18)
        self.isVisible = True
        pygame.time.set_timer(pygame.USEREVENT, 2000)

    def end(self):
        self.game.alerts.remove(self)

    def blit(self):
        if self.isVisible:
            text = self.font.render(self.text, False, self.color)
            self.game.surface. blit(text, (100, self.game.vh - 300))
