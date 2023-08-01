import pygame


class Interface:

    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = image

    def blit(self):
        self.screen.blit(self.image, (self.x, self.y))
        #text = self.font.render(f'{self.npc_name}: {self.texts[self.text_index][0:self.letter_index]}', False, (0, 0, 0))
        #self.screen.blit(text, (self.X_POSITION + 50, self.Y_POSITION + 20))
