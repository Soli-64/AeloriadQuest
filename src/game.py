import pygame, pyscroll.data, pytmx.util_pygame
from src.map import MapManager
from src.player import Player
from src.Weapons.weapon import Weapon
from src.Weapons.fire_weapon import FireWeapon
from src.Enemy.enemy import Enemy
from src.Items.interface import Interface, Screen_Point
from src.Utils.pygame_functions import pygame_image

class Game:

    def __init__(self):
        self.surface = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("RpgGameMission")
        self.player = Player(self)
        self.map_manager = MapManager(self.surface, self.player)
        self.player.add_weapons(
            [Weapon('sword', 1, self.map_manager, self),
             FireWeapon('gun', 1, self.map_manager, self.player)]
        )
        self.inventory = Interface(self.surface, 220, 50, pygame_image('./images/interfaces/inventory.png', [800, 550]))
        self.barre_interface = Interface(self.surface, 20, 20, pygame_image('./images/interfaces/left_interface.png', [250, 500]))
        self.current_weapons_points = [ Screen_Point(120, 348, [50, 50]), Screen_Point(35, 368, [50, 50]), Screen_Point(205, 368, [50, 50]) ]

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

            if inventory:
                self.inventory.blit()
                for w in self.player.weapons:
                    w.blit_inventory_image()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.run()
                        break

            clock.tick(60)

    pygame.quit()

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:

            self.player.save_location()
            self.handle_input()
            self.map_manager.draw()
            # Interfaces
            self.barre_interface.blit()
            for p in self.player.projectiles:
                p.blit(self.surface)
                p.move()
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
                    elif event.key == pygame.K_1:
                        self.player.choice_current_weapon(0)
                    elif event.key == pygame.K_2:
                        self.player.choice_current_weapon(1)

            clock.tick(60)
        pygame.quit()
