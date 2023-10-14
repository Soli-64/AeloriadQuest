import pygame, pygame_gui as pg_gui
import src.Utils.pg_utils as f_pg
import src.Utils.colors as co, json, sys
from threading import Thread
from pygame.locals import *
from src.Elements.market import Market
from src.map import MapManager
from src.player import Player
from src.Weapons.weapon import Weapon
from src.Weapons.FireWeapon.fire_weapon import FireWeapon
from src.Elements.interface import Interface, Alert
from src.Dialogs.dialog import DialogBox
from src.Utils.settings import *
from src.Utils.config import load_config
from src.Elements.element import *
from src.Elements.menu import Menu
from src.Elements.inventory import Inventory
from src.Enemy.enemy import DamagedNumber

class Game:

    def __init__(self):

        # Game motors elements

        self.game_config = load_config('./config.txt', ['LANG', 'SCREEN_WIDTH', 'SCREEN_HEIGHT'])

        self.isPlaying = False
        self.isDied = False
        self.lang = self.game_config['LANG']
        self.get_game_texts()

        self.game_running = True

        self.traders_random_stuffs = False
        self.missioners_occuped_position = []

        self.event_buttons = {}

        # Window elements
        self.vw = int(self.game_config['SCREEN_WIDTH'])
        self.vh = int(self.game_config['SCREEN_HEIGHT'])
        self.surface = pygame.display.set_mode((self.vw, self.vh), RESIZABLE)
        pygame.display.set_caption("AeloriadQuest")

        # Instances
        self.player = Player(self)
        self.map_manager = MapManager(self.surface, self.player, self)

        # Instances Manipulations
        self.player.add_weapons([
            Weapon('sword', 1, self.map_manager),
            FireWeapon('gun', 1, self.map_manager)
        ])
        self.player.set_manager(self.map_manager)

        # Inventory
        self.inventory = Inventory(self, self.surface, self.player)

        # Market
        self.market = Market(self, self.surface, self.player)

        # Dialog_box
        self.dialog_box = DialogBox(self)

        # Graphic elements
        self.ui_manager = pg_gui.UIManager(self.surface.get_size())

        self.panel_buttons = Element(name='Panel',
                                     rect=[(200, 0), (400, 300)],
                                     ui_manager=self.ui_manager,
                                     object_id='',
                                     container=None
                                     ).UI

        self.play_btn = EventButton(
            rect=[(100, 100), (300, 100)],
            text='Play',
            ui_manager=self.ui_manager,
            object_id='#play_button',
            container=self.panel_buttons,
            func=lambda: self.start()
        )

        self.event_buttons['#play_button'] = self.play_btn
        self.coin_box = Interface(self.surface, COIN_BOX(self.vw), f_pg.pygame_image('./assets/images/interfaces/coin_box.png', [200, 80]), [])
        self.died_bg = Interface(self.surface, [0, 0], f_pg.pygame_image('./assets/images/menu/died_background.png', [self.vw, self.vh]), [])
        self.alerts = []

        # Events declarations
        pygame.time.set_timer(RESET_TRADERS_STUFF, 1000)

        # Init declarations
        self.res_btn = None
        self.res_btn_rect = None
        self.play_btn_rect = None

    def start(self): self.isPlaying = True

    def end(self): self.isPlaying = False

    def set_traders_stuff(self):
        for t in self.map_manager.get_map().traders:
            t.create_random_stuff()

    def died(self):
        self.isDied = True
        self.UI_pause()

    def get_map_type(self):
        with open('./assets/json/maps.json', 'r') as file:
            data = json.load(file)
        return data[self.map_manager.current_map]

    def get_game_texts(self):
        with open('./assets/json/elements_text.json', 'r') as file:
            data = json.load(file)
            self.texts = data[self.lang]

    def respawn(self):
        self.player.remove_money(30)
        self.map_manager.current_map = 'city'
        self.map_manager.teleport_player('player')
        self.player.health = self.player.max_health
        self.run()

    def resize(self, w, h):
        # A voir self.map_manager.set_map_layer_size()
        self.vw, self.vh = w, h

        self.inventory.resize(self.surface)
        self.inventory.draw_items(self.inventory.focus)

        self.market.resize(self.surface)

        self.surface = pygame.display.set_mode((self.vw, self.vh), RESIZABLE)

        self.dialog_box.X_POS = self.vw / 4
        self.dialog_box.Y_POS = self.vh - 130

        self.died_bg = Interface(self.surface, [0, 0], f_pg.pygame_image('./assets/images/menu/died_background.png', [self.vw, self.vh]), [])
        self.coin_box = Interface(self.surface, COIN_BOX(self.vw), f_pg.pygame_image('./assets/images/interfaces/coin_box.png', [200, 80]), [])
        self.w_case = Interface(self.surface, WEAPON_CASE(self.vw, self.vh), f_pg.pygame_image('./assets/images/interfaces/weapon_case.png', [200, 200]), [])

    def update(self): self.map_manager.update()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]: self.player.move_up()

        elif pressed[pygame.K_LEFT]: self.player.move_left()

        elif pressed[pygame.K_RIGHT]: self.player.move_right()

        elif pressed[pygame.K_DOWN]:self.player.move_down()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.game_running = False
        # Resize the window
        elif event.type == VIDEORESIZE:
            self.resize(event.w, event.h)
        elif event.type == REMOVE_ALERTS:
            for a in self.alerts: a.end()
        # Events button
        elif event.type == RESET_TRADERS_STUFF:
            self.set_traders_stuff()
        self.inventory.ui_manager.process_events(event)
        self.market.ui_manager.process_events(event)
        self.ui_manager.process_events(event)
        if event.type == pg_gui.UI_BUTTON_START_PRESS:
            bouton_id = event.ui_element.object_ids[len(event.ui_element.object_ids) - 1]
            for key in self.event_buttons.keys():
                if bouton_id == key:
                    self.event_buttons[key].execute()

    def UI_inventory(self):
        clock = pygame.time.Clock()
        self.dialog_box.reading = False

        self.game_running = True
        while self.game_running:

            time_delta = clock.tick(60) / 1000.0

            self.map_manager.draw()

            # Interfaces
            self.coin_box.blit()
            # Append of player stats
            pygame.draw.rect(self.surface, (255, 255, 255), (20, 20, 100, 140), 4)
            self.player.update_stats(self.surface)

            if self.inventory.visible_info_zone:
                self.inventory.info_zone()

            self.inventory.update(time_delta)
            self.inventory.draw()

            pygame.display.flip()

            for event in pygame.event.get():

                self.handle_events(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or pygame.K_b:
                        self.run()

                # If window is resized
                elif event.type == VIDEORESIZE:
                    self.resize(event.w, event.h)
                # Close Inventoy or Market
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or pygame.K_b:
                        self.run()

        pygame.quit()
        sys.exit()

    def UI_market(self):

        clock = pygame.time.Clock()

        self.game_running = True
        while self.game_running:

            time_delta = clock.tick(60) / 1000.0

            self.map_manager.draw()

            # Interfaces
            self.coin_box.blit()
            # Append of player stats
            pygame.draw.rect(self.surface, (255, 255, 255), (20, 20, 100, 140), 4)
            self.player.update_stats(self.surface)

            self.market.update(time_delta)
            self.market.draw()

            pygame.display.flip()

            for event in pygame.event.get():

                self.handle_events(event)

                # Close Market
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or pygame.K_b:
                        self.run()

        pygame.quit()
        sys.exit()

    def UI_pause(self):
        clock = pygame.time.Clock()

        self.game_running = True
        while self.game_running:

            # time delta set for PygameGui
            time_delta = clock.tick(60) / 1000.0

            # Map, player and enemies drawing
            self.map_manager.draw()

            if self.isDied:
                self.died_bg.blit()
                self.res_btn = f_pg.pygame_image('./assets/images/menu/resurrect_button.png', [self.vw / 3.33, self.vw / 9.99])
                self.res_btn_rect = self.res_btn.get_rect()
                self.res_btn_rect.x = self.vw / 3
                self.res_btn_rect.y = (self.vh / 4) * 3
                self.surface.blit(self.res_btn, (self.vw / 3, (self.vh / 4 * 3)))

            pygame.display.flip()

            for event in pygame.event.get():

                self.handle_events(event)

                # If player is died
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.isDied:
                        if self.res_btn_rect.collidepoint(event.pos):
                            self.respawn()
                            break
                # Close Inventoy or Market
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or pygame.K_b:
                        self.run()

        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()

        self.game_running = True
        while self.game_running:
            time_delta = clock.tick(60)
            if self.isPlaying:

                self.player.save_location()
                self.handle_input()
                self.map_manager.draw()
                self.dialog_box.render(self.surface)
                # Interfaces
                pygame.draw.rect(self.surface, co.WHITE, (20, 20, 100, 140), 4)
                self.coin_box.blit()

                if self.player.selected_weapon:
                    self.surface.blit(self.player.selected_weapon.item_image, SELECTED_WEAPON(self.vw, self.vh))
                    self.surface.blit(f_pg.text(self.player.selected_weapon.munitions, None, 30, co.WHITE), MUNITION_NUMBER(self.vw, self.vh))

                if self.get_map_type() == 'dungeon':
                    self.player.set_weapon_image()
                    self.surface.blit(
                                    f_pg.text(f'{len(self.map_manager.get_map().enemys)} / {self.map_manager.current_mission.n_enemy}',
                                                None,
                                                65,
                                                co.WHITE),
                                    ((self.vw / 2) - 20, self.vh - 50)
                                    )

                for alert in self.alerts:
                    if type(alert) is DamagedNumber:
                        alert.move()

                # Game update
                self.update()

            else:
                # Background
                bg = f_pg.pygame_image('./assets/images/menu/background.png', [self.vw, self.vh])
                self.surface.blit(bg, (0, 0))

                # Pygame Gui
                """self.game_menu.update(time_delta)
                self.game_menu.draw()"""
                self.ui_manager.update(time_delta)
                self.ui_manager.draw_ui(self.surface)

            # Window update
            pygame.display.flip()

            # Events management
            for event in pygame.event.get():

                self.player.weapon_animation.handle_event(event)
                self.handle_events(event)

                """if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_btn_rect.collidepoint(event.pos):
                        self.start()"""

                if event.type == pygame.KEYDOWN:
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
                            self.inventory.draw_items(self.inventory.focus)
                            self.UI_inventory()
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