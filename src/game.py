import pygame, pyscroll.data, pytmx.util_pygame
from src.map import MapManager
from src.player import Player
from src.Items.interface import Interface
from src.Utils.pygame_functions import pygame_image

class Game:

    def __init__(self):
        self.surface = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("RpgGameMission")
        self.player = Player(self)
        self.map_manager = MapManager(self.surface, self.player)

        self.inventory = Interface(self.surface, 220, 50, pygame_image('./elements/interfaces/inventory.png', [800, 550]))
        self.barre_interface = Interface(self.surface, 20, 20, pygame_image('./elements/interfaces/left_interface.png', [250, 500]))

    def update(self):
        self.map_manager.update()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()

        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

        elif pressed[pygame.K_DOWN]:
            self.player.move_down()

    def pause(self, inventory):
        clock = pygame.time.Clock()

        running = True
        while running:

            self.map_manager.draw()

            if inventory: self.inventory.blit()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run()
                        break

            clock.tick(60)




    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:


            self.player.save_location()
            self.handle_input()
            self.map_manager.draw()
            # Interfaces
            self.barre_interface.blit()
            #
            self.update()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.attack()
                    elif event.key == pygame.K_v:
                        self.map_manager.check_missioner_collision()
                    elif event.key == pygame.K_b:
                        self.pause(True)
                        break


            clock.tick(60)

        pygame.quit()
