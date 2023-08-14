import pygame
import src.Utils.pygame_functions as f_pg

class DialogBox:

    def __init__(self, game):
        self.game = game
        self.X_POS = self.game.vw / 5
        self.Y_POS = self.game.vh - 110
        self.box = f_pg.pygame_image('./assets/images/interfaces/dialog_box.png', [850, 100])
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('./assets/fonts/dialog_font.ttf', 18)
        self.reading = False
        self.missioner_name = 'default'

    def execute(self, missioner):
        self.missioner = missioner
        self.missioner_name = missioner.name
        if self.reading:
            return self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = missioner.dialog

    def render(self, screen):
        if self.reading:
            self.letter_index += 1
            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
            screen.blit(self.box, (self.X_POS, self.Y_POS))
            text = self.font.render(f'{self.missioner_name}: {self.texts[self.text_index][0:self.letter_index]}', False, (0, 0, 0))
            screen.blit(text, (self.X_POS + 75, self.Y_POS + 20))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            # close dialog
            self.reading = False
            self.missioner.launch_mission()
            return self.missioner.mission

