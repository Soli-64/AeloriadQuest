import pygame, pyscroll.data, pytmx.util_pygame
from src.map import MapManager
from src.player import Player
from src.Weapons.weapon import Weapon
from src.Weapons.magic_weapon import MagicWeapon
from src.Enemy.enemy import Enemy
from src.Utils.interface import Interface, Screen_Point
from src.Dialogs.dialog import DialogBox
import src.Utils.pygame_functions as f_pg

class Game:

    def __init__(self):
        self.surface = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("RpgGameMission")
        self.player = Player(self)
        self.map_manager = MapManager(self.surface, self.player )
        self.player.add_weapons(
            [ Weapon('sword', 1, self.map_manager, self.player),
              MagicWeapon('gun', 1, self.map_manager, self.player)]
        )
        self.dialog_box = DialogBox()
        self.inventory = Interface(self.surface, 220, 50, f_pg.pygame_image('./assets/images/interfaces/inventory.png', [800, 550]), [])
        self.coin_box = Interface(self.surface, 930, 10, f_pg.pygame_image('./assets/images/interfaces/coin_box.png', [200, 80]), [])

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

            # dessin de la map, du joueur et des enemy
            self.map_manager.draw()


            if inventory: self.inventory.blit()

            pygame.draw.rect(self.surface, (255, 255, 255), (20, 20, 100, 140), 4)

            # Interfaces
            self.coin_box.blit()

            # Ajout des stats du player
            self.player.update_stats(self.surface)


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
        black = (0, 0, 0)
        white = (255, 255, 255)

        running = True
        while running:

            self.player.save_location()
            self.handle_input()
            self.map_manager.draw()
            self.dialog_box.render(self.surface)
            # Interfaces
            pygame.draw.rect(self.surface, white, (20, 20, 100, 140), 4)
            self.coin_box.blit()
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
                        self.map_manager.check_missioner_collision(self.dialog_box)
                    elif event.key == pygame.K_b:
                        self.pause(True)
                        break
                    elif event.key == pygame.K_g:
                        self.map_manager.check_chest_collision()
                    elif event.key == pygame.K_1:
                        self.player.choice_current_weapon(0)
                    elif event.key == pygame.K_2:
                        self.player.choice_current_weapon(1)

            clock.tick(60)
        pygame.quit()
