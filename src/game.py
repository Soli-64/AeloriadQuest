import threading

import pygame, pygame_gui as pg_gui
from threading import Thread
import src.Utils.colors as co, json, sys
from pygame.locals import *
from src.map import MapManager
from src.player import Player
from src.Weapons.weapon import Weapon
from src.Weapons.FireWeapon.fire_weapon import FireWeapon
from src.Elements.interface import Interface, Alert
from src.Dialogs.dialog import DialogBox
import src.Utils.pg_utils as f_pg
from src.Utils.settings import *
from src.Elements.menu import Menu
from src.Elements.inventory import Inventory
from src.Enemy.enemy import DamagedNumber

class Game:

    def __init__(self):

        # Motors elements of the game
        self.isPlaying = False
        self.isDied = False
        self.lang = LANG
        self.get_text()
        self.missioners_occupied_position = []

        # Window elements
        self.vw = 1200
        self.vh = 700
        self.surface = pygame.display.set_mode((self.vw, self.vh), RESIZABLE)
        pygame.display.set_caption("AeloriadQuest")

        # Instances
        self.player = Player(self)
        self.map_manager = MapManager(self.surface, self.player, self)

        # Instances Manipulations
        self.player.add_weapons([
            Weapon('sword', 1, self.map_manager, self.player, './assets/images/sprite/slash/slash_effect_anim_f0.png'),
            FireWeapon('gun', 1, self.map_manager, self.player, './assets/images/sprite/slash/slash_effect_anim_f0.png')
        ])
        self.player.set_manager(self.map_manager)

        # Inventory
        self.i = Inventory(self.surface, self.player)

        # Graphic elements
        self.game_menu = Menu(self.surface, [
                            {
                                'name': 'Panel',
                                'text': '',
                                'rect': [(200, 50), (200, 500)],
                                'object_id': '',
                                'container': None
                            },
                            {
                                'name': 'Button',
                                'text': self.texts['buttons']['play_button'],
                                'rect': [(200, 200), (200, 50)],
                                'object_id': 'button',
                                'container': None
                            },
                            {
                                'name': 'Button',
                                'text': self.texts['buttons']['settings_button'],
                                'rect': [(200, 300), (200, 50)],
                                'object_id': 'button',
                                'container': None
                            }
                        ])

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
        self.alerts = []

        # Init declarations
        self.res_btn = None
        self.res_btn_rect = None
        self.play_btn_rect = None

    def start(self): self.isPlaying = True

    def end(self): self.isPlaying = False

    def died(self):
        self.isDied = True
        self.pause(False, False)


    def get_map_type(self):
        with open('./assets/json/maps.json', 'r') as file:
            data = json.load(file)
        return data[self.map_manager.current_map]

    def get_text(self):
        with open('./assets/json/elements_text.json', 'r') as file:
            data = json.load(file)
            self.texts = data[self.lang]

    def respawn(self):
        self.player.remove_money(30)
        self.map_manager.current_map = 'world'
        self.map_manager.teleport_player('player')
        self.player.health = self.player.max_health
        self.run()

    def resize(self, w, h):
        self.vw, self.vh = w, h
        self.i.resize(self.surface)
        self.i.draw_items(self.i.focus)
        self.surface = pygame.display.set_mode((self.vw, self.vh), RESIZABLE)
        self.dialog_box.X_POS = self.vw / 4
        self.dialog_box.Y_POS = self.vh - 130
        self.inventory = Interface(self.surface, [220, 50], f_pg.pygame_image('./assets/images/interfaces/inventory.png', [(self.vw / 3) * 2, (self.vh / 10) * 8]), [])
        self.died_bg = Interface(self.surface, [0, 0], f_pg.pygame_image('./assets/images/menu/died_background.png', [self.vw, self.vh]), [])
        self.coin_box = Interface(self.surface, COIN_BOX(self.vw), f_pg.pygame_image('./assets/images/interfaces/coin_box.png', [200, 80]), [])
        self.w_case = Interface(self.surface, WEAPON_CASE(self.vw, self.vh), f_pg.pygame_image('./assets/images/interfaces/weapon_case.png', [200, 200]), [])
        self.market = Interface(self.surface, MARKET(self.vw, self.vh), f_pg.pygame_image('./assets/images/interfaces/market/market.png', [self.vw / 1.3, self.vh]), [])

    def update(self): self.map_manager.update()

    def r_map_manager(self): return self.map_manager

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

            # Time Delta set for PygameGui
            time_delta = clock.tick(60) / 1000.0

            # Map, player and enemies drawing
            self.map_manager.draw()

            if inventory:

                # Inventory
                self.inventory.blit()
                # Interfaces
                self.coin_box.blit()
                # Append of player stats
                pygame.draw.rect(self.surface, (255, 255, 255), (20, 20, 100, 140), 4)
                self.player.update_stats(self.surface)

                if self.i.visible_info_zone:
                    self.i.info_zone()

                self.i.update(time_delta)
                self.i.draw()

            elif self.isDied:
                self.died_bg.blit()
                self.res_btn = f_pg.pygame_image('./assets/images/menu/resurrect_button.png', [self.vw / 3.33, self.vw / 9.99])
                self.res_btn_rect = self.res_btn.get_rect()
                self.res_btn_rect.x = self.vw / 3
                self.res_btn_rect.y = (self.vh / 4) * 3
                self.surface.blit(self.res_btn, (self.vw / 3, (self.vh / 4 * 3)))

            elif market:
                self.market.blit()

            pygame.display.flip()

            for event in pygame.event.get():
                # Close Window
                if event.type == pygame.QUIT:
                    running = False
                # If player is died
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.isDied:
                        if self.res_btn_rect.collidepoint(event.pos):
                            self.respawn()
                            break
                 # If window is resized
                elif event.type == VIDEORESIZE:
                    self.resize(event.w, event.h)
                # Close Inventoy or Market
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or pygame.K_b:
                        self.run()

                inventory = True
                if inventory:
                    self.i.ui_manager.process_events(event)
                    if event.type == pg_gui.UI_BUTTON_START_PRESS:
                        bouton_id = event.ui_element.object_ids[len(event.ui_element.object_ids) - 1]
                        for key in self.i.event_buttons.keys():
                            if bouton_id == key:
                                self.i.event_buttons[key].execute()
                        """for element in self.i.buttons:
                            if bouton_id == element.object_id.object_id:
                                element.execute()"""

        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            time_delta = clock.tick(60)
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
                    self.player.set_weapon_image()
                    self.surface.blit(
                                    f_pg.text(f'{len(self.map_manager.get_map().enemys)} / {self.map_manager.current_mission.n_enemy}',
                                                None,
                                                35,
                                                co.WHITE),
                                    ((self.vw / 2) - 20, self.vh - 50)
                                    )

                """for type in self.types:
                    pass
                    type.blit()"""
                for alert in self.alerts:
                    if type(alert) is DamagedNumber:
                        alert.move()

                # Game update
                self.update()

            else:
                # PyGame Elements

                # Background
                bg = f_pg.pygame_image('./assets/images/menu/background.png', [self.vw, self.vh])
                self.surface.blit(bg, (0, 0))

                # Pygame Gui
                self.game_menu.update(time_delta)
                self.game_menu.draw()

                # Play button
                self.play_btn_rect = self.game_menu.elems[1].rect
                self.settings_btn_rect = self.game_menu.elems[1].rect

            # Window update
            pygame.display.flip()

            # Events management
            for event in pygame.event.get():

                self.player.weapon_animation.handle_event(event)

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
                        self.map_manager.check_trader_collision(self)

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

        pygame.quit()
        sys.exit()