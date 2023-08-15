import pygame, src.Utils.colors as co, time, json, sys
from pygame.locals import *
from src.map import MapManager
from src.player import Player
from src.Weapons.weapon import Weapon
from src.Weapons.fire_weapon import FireWeapon
from src.Utils.interface import Interface, Alert
from src.Dialogs.dialog import DialogBox
import src.Utils.pygame_functions as f_pg
from src.Utils.settings import *


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
              FireWeapon('gun', 1, self.map_manager, self.player)]
        )
        # éléments graphiques
        self.dialog_box = DialogBox(self)
        self.inventory = Interface(self.surface, INVENTORY(), f_pg.pygame_image('./assets/images/interfaces/inventory.png', [(self.vw / 3) * 2, (self.vh / 10) * 8]), [])
        self.coin_box = Interface(self.surface, COIN_BOX(self.vw), f_pg.pygame_image('./assets/images/interfaces/coin_box.png', [200, 80]), [])
        self.died_bg = Interface(self.surface, [0, 0], f_pg.pygame_image('./assets/images/menu/died_background.png', [self.vw, self.vh]), [])
        self.w_case = Interface(self.surface, WEAPON_CASE(self.vw, self.vh), f_pg.pygame_image('./assets/images/interfaces/weapon_case.png', [200, 200]), [])
        self.market = Interface(self.surface, MARKET(self.vw, self.vh), f_pg.pygame_image('./assets/images/interfaces/market/market.png', [self.vw / 1.3, self.vh]), [])
        self.types = [
            Interface(self.surface, [50, 200], f_pg.pygame_image('./assets/images/interfaces/type/type_e.png', [120, 70]), []),
            Interface(self.surface, [50, 300], f_pg.pygame_image('./assets/images/interfaces/type/type_z.png', [120, 80]), [])
        ]
        self.alerts = [
            Alert(self, 'Hello World', co.WHITE, 0)
        ]
        #self.get_map_type()

    def start(self): self.isPlaying = True

    def end(self): self.isPlaying = False

    def died(self):
        self.isDied = True
        self.pause(False)

    def get_map_type(self):
        with open('./assets/json/maps.json', 'r') as file:
            data = json.load(file)
        return data[self.map_manager.current_map]

    def respawn(self):
        self.player.remove_money(30)
        self.map_manager.current_map = 'world'
        self.map_manager.teleport_player('player')
        self.player.health = self.player.max_health
        self.run()

    def resize(self, w, h):
        self.vw, self.vh = w, h
        self.surface = pygame.display.set_mode((self.vw, self.vh), RESIZABLE)
        self.dialog_box.X_POS = self.vw / 4
        self.dialog_box.Y_POS = self.vh - 130
        self.inventory = Interface(self.surface, [220, 50], f_pg.pygame_image('./assets/images/interfaces/inventory.png', [(self.vw / 3) * 2, (self.vh / 10) * 8]), [])
        self.died_bg = Interface(self.surface, [0, 0], f_pg.pygame_image('./assets/images/menu/died_background.png', [self.vw, self.vh]), [])
        self.coin_box = Interface(self.surface, COIN_BOX(self.vw), f_pg.pygame_image('./assets/images/interfaces/coin_box.png', [200, 80]), [])
        self.w_case = Interface(self.surface, WEAPON_CASE(self.vw, self.vh), f_pg.pygame_image('./assets/images/interfaces/weapon_case.png', [200, 200]), [])
        self.market = Interface(self.surface, MARKET(self.vw, self.vh), f_pg.pygame_image('./assets/images/interfaces/market/market.png', [self.vw / 1.3, self.vh]), [])

    def update(self): self.map_manager.update()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]: self.player.move_up()

        elif pressed[pygame.K_LEFT]: self.player.move_left()

        elif pressed[pygame.K_RIGHT]: self.player.move_right()

        elif pressed[pygame.K_DOWN]:self.player.move_down()

    def pause(self, inventory=False, market=False):
        clock = pygame.time.Clock()

        running = True
        while running:

            # dessin de la map, du joueur et des enemy
            self.map_manager.draw()

            if inventory:
                # Inventaire
                self.inventory.blit()
                # Interfaces
                self.coin_box.blit()
                # Ajout des stats du player
                pygame.draw.rect(self.surface, (255, 255, 255), (20, 20, 100, 140), 4)
                self.player.update_stats(self.surface)

            elif self.isDied:
                self.died_bg.blit()
                self.res_btn = f_pg.pygame_image('./assets/images/menu/resurect_button.png', [self.vw / 3.33, self.vw / 9.99])
                self.res_btn_rect = self.res_btn.get_rect()
                self.res_btn_rect.x = self.vw / 3
                self.res_btn_rect.y = (self.vh / 4) * 3
                self.surface.blit(self.res_btn, (self.vw / 3, (self.vh / 4 * 3)))

            elif market:
                self.market.blit()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.isDied:
                        if self.res_btn_rect.collidepoint(event.pos):
                            self.respawn()
                            break
                elif event.type == VIDEORESIZE:
                    self.resize(event.w, event.h)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or pygame.K_b:
                        self.run()
                        break

            clock.tick(60)
        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            if self.isPlaying:

                self.player.save_location()
                self.handle_input()
                self.map_manager.draw()
                self.dialog_box.render(self.surface)
                # Interfaces
                pygame.draw.rect(self.surface, co.WHITE, (20, 20, 100, 140), 4)
                self.coin_box.blit()
                self.w_case.blit()

                if self.player.selected_weapon:
                    self.surface.blit(self.player.selected_weapon.item_image, SELECTED_WEAPON(self.vw, self.vh))
                    self.surface.blit(f_pg.text(self.player.selected_weapon.munitions, None, 30, co.WHITE), MUNITION_NUMBER(self.vw, self.vh))

                if self.get_map_type() == 'dungeon':
                    self.surface.blit(f_pg.text(f'l{len(self.map_manager.get_map().enemys)} / {self.map_manager.current_mission.n_enemy}', None, 35, co.WHITE), ((self.vw / 2) - 20, self.vh - 50))

                """for type in self.types:
                    pass
                    type.blit()"""
                for alert in self.alerts:
                    alert.blit()

                # Update du jeu
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

            # mise a jour de la fenêtre
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT:
                    for alert in self.alerts:
                        alert.end()
                elif event.type == VIDEORESIZE:
                    self.resize(event.w, event.h)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_btn_rect.collidepoint(event.pos):
                        self.start()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.attack('')
                    elif event.key == pygame.K_z:
                        self.player.attack('magic')
                    elif event.key == pygame.K_e:
                        self.player.attack('fire')
                    elif event.key == pygame.K_v:
                        self.map_manager.check_missioner_collision(self.dialog_box)
                        self.map_manager.check_traider_collision(self)
                    elif event.key == pygame.K_b:
                        if self.isPlaying:
                            self.pause(True, False)
                            break
                    elif event.key == pygame.K_f:
                        self.map_manager.check_chest_collision()
                    elif event.key == pygame.K_ESCAPE:
                        self.dialog_box.reading = False
                    elif event.key == pygame.K_1:
                        self.player.choice_current_weapon(0)
                    elif event.key == pygame.K_2:
                        self.player.choice_current_weapon(1)

            clock.tick(60)
        pygame.quit()
        sys.exit()