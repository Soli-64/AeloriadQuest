import pygame, pyscroll.data, pytmx.util_pygame, math
from pygame.locals import *
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
        # éléments du moteur du jeu
        self.isPlaying = False
        self.isDied = False
        self.vw = 1200
        self.vh = 700
        self.surface = pygame.display.set_mode((self.vw, self.vh), RESIZABLE)
        pygame.display.set_caption("RpgMission")
        # Instances
        self.player = Player(self)
        self.map_manager = MapManager(self.surface, self.player )

        # Manipulations des Instances
        self.player.add_weapons(
            [ Weapon('sword', 1, self.map_manager, self.player),
              MagicWeapon('gun', 1, self.map_manager, self.player)]
        )
        # éléments graphiques
        self.dialog_box = DialogBox()
        self.inventory = Interface(self.surface, 220, 50, f_pg.pygame_image('./assets/images/interfaces/inventory.png', [(self.vw / 3) * 2, (self.vh / 10) * 8]), [])
        self.coin_box = Interface(self.surface, (self.vw - 270), 10, f_pg.pygame_image('./assets/images/interfaces/coin_box.png', [200, 80]), [])
        self.died_bg = Interface(self.surface, 0, 0, f_pg.pygame_image('./assets/images/menu/died_background.png', [self.vw, self.vh]), [])

    def start(self): self.isPlaying = True

    def end(self): self.isPlaying = False

    def died(self):
        self.isDied = True
        self.pause(False)

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

            if inventory:
                self.inventory.blit()
                pygame.draw.rect(self.surface, (255, 255, 255), (20, 20, 100, 140), 4)

                # Interfaces
                self.coin_box.blit()

                # Ajout des stats du player
                self.player.update_stats(self.surface)

            elif self.isDied:
                self.died_bg.blit()


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

            if self.isPlaying:

                self.player.save_location()
                self.handle_input()
                self.map_manager.draw()
                self.dialog_box.render(self.surface)
                # Interfaces
                pygame.draw.rect(self.surface, white, (20, 20, 100, 140), 4)
                self.coin_box.blit()
                #
                self.update()

            else:
                # éléments pygame

                # background
                bg = f_pg.pygame_image('./assets/images/menu/background.png', [self.vw, self.vh])
                self.surface.blit(bg, (0, 0))
                # play button
                self.play_btn = f_pg.pygame_image('./assets/images/menu/play_btn.png', [150, 50])
                self.play_btn_rect = self.play_btn.get_rect()
                self.play_btn_rect.x = 100 #math.ceil(self.surface.get_width() / 2)
                self.play_btn_rect.y = 400 #math.ceil(self.surface.get_height() / 3.33)
                self.surface.blit(self.play_btn, (100, 400))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == VIDEORESIZE:
                    self.vw, self.vh = event.w, event.h
                    self.surface = pygame.display.set_mode((self.vw, self.vh), RESIZABLE)
                    self.inventory = Interface(self.surface, 220, 50, f_pg.pygame_image('./assets/images/interfaces/inventory.png', [(self.vw / 3) * 2, (self.vh / 10) * 8]), [])
                    self.died_bg = Interface(self.surface, 0, 0, f_pg.pygame_image('./assets/images/menu/died_background.png', [self.vw, self.vh]), [])

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print('test')
                    if self.play_btn_rect.collidepoint(event.pos):
                        print('test')
                        self.start()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.attack()
                    elif event.key == pygame.K_v:
                        self.map_manager.check_missioner_collision(self.dialog_box)
                    elif event.key == pygame.K_b:
                        if self.isPlaying:
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
