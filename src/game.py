import pygame, pygame_gui as pg_gui
import src.Utils.pg_utils as utils
import src.Utils.colors as co, json, sys
from pygame.locals import *
from src.Elements.market import Market
from src.map import MapManager
from src.player import Player
from src.Weapons.weapon import Weapon
from src.Weapons.FireWeapon.fire_weapon import FireWeapon
from src.Weapons.FireWeapon.charger import Charger
from src.Elements.interface import Interface, Alert
from src.Dialogs.dialog import DialogBox
from src.Utils.settings import *
from src.Elements.element import *
from src.Elements.inventory import Inventory
from src.Enemy.enemy import DamagedNumber

class Game:

    def __init__(self):

        # Game motors elements

        self.game_config = self.load_config('./assets/config.txt', ['LANG', 'SCREEN_WIDTH', 'SCREEN_HEIGHT'])

        self.isPlaying = False
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
        self.player.add_objects([
            Weapon('sword', 1, self.map_manager),
            FireWeapon('gun', 1, self.map_manager)
        ], 'weapons')
        self.player.add_objects([
            Charger(self.map_manager, "normal")
        ], 'chargers')
        self.player.select_weapons([0, 1])
        self.player.set_manager(self.map_manager)

        # Inventory
        self.inventory = Inventory(self, self.surface, self.player)

        # Market
        self.market = Market(self, self.surface, self.player)

        # Dialog_box
        self.dialog_box = DialogBox(self)

        # Graphic elements
        self.ui_manager = pg_gui.UIManager(self.surface.get_size(), './assets/json/graffics/game-menu/style.json')

        self.coin_box = Interface(self.surface, COIN_BOX(self.vw), utils.pygame_image('./assets/images/interfaces/coin_box.png', [200, 80]), [])
        self.w_case = Interface(self.surface, WEAPON_CASE(self.vw, self.vh), utils.pygame_image('./assets/images/interfaces/weapon_case.png', [200, 200]), [])
        self.alerts = []

        # Events declarations
        pygame.time.set_timer(RESET_TRADERS_STUFF, 15000)

        # Init declarations
        self.res_btn = None
        self.res_btn_rect = None

    def start(self): self.isPlaying = True

    def end(self): self.isPlaying = False

    def set_traders_stuff(self):
        for trader in self.map_manager.get_map().traders:
            trader.create_random_stuff()

    def died(self):
        self.UI_died()

    def get_map_type(self):
        with open('./assets/json/maps.json', 'r') as file:
            data = json.load(file)
        return data[self.map_manager.current_map]

    def get_game_texts(self):
        with open('./assets/json/elements_text.json', 'r') as file:
            data = json.load(file)
            self.texts = data[self.lang]

    def load_config(self, file_path: str, values: [str]):
        config = {}
        with open(file_path, 'r') as file:
            for val in values:
                file.seek(0)
                section_name = val
                for line in file:
                    line = line.strip()
                    line_name = line.split('=')[0]
                    if line_name == val:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        return config

    def respawn(self):
        self.player.remove_money(30)
        self.map_manager.current_map = 'city'
        self.map_manager.teleport_player('player')
        self.player.health = self.player.max_health
        self.run()

    def resize(self, w, h):
        # A voir self.map_manager.set_map_layer_size()
        self.vw, self.vh = w, h

        # game menu

        self.panel_buttons = Element(name='Panel',
                                     rect=[(-5, -5), (self.surface.get_width() + 10, self.surface.get_height() + 10)],
                                     ui_manager=self.ui_manager,
                                     object_id=Ids(_class_id='@panel', _object_id='#mainpanel').all,
                                     container=None
                                     ).UI

        self.play_btn = EventButton(
            rect=[(100, 100), (300, 100)],
            text=self.texts['buttons']['play'],
            ui_manager=self.ui_manager,
            object_id=Ids(_class_id='@button', _object_id='#play_button').all,
            container=self.panel_buttons,
            func=lambda: self.start()
        )

        self.event_buttons['#play_button'] = self.play_btn

        self.inventory.resize()
        self.inventory.draw_items(self.inventory.focus)

        self.market.resize()

        self.surface = pygame.display.set_mode((self.vw, self.vh), RESIZABLE)

        self.dialog_box.X_POS = self.vw / 4
        self.dialog_box.Y_POS = self.vh - 130

        self.coin_box = Interface(self.surface, COIN_BOX(self.vw), utils.pygame_image('./assets/images/interfaces/coin_box.png', [200, 80]), [])
        self.w_case = Interface(self.surface, WEAPON_CASE(self.vw, self.vh), utils.pygame_image('./assets/images/interfaces/weapon_case.png', [200, 200]), [])

    def update(self): self.map_manager.update()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]: self.player.move_up()

        elif pressed[pygame.K_LEFT]: self.player.move_left()

        elif pressed[pygame.K_RIGHT]: self.player.move_right()

        elif pressed[pygame.K_DOWN]:self.player.move_down()

    def handle_events(self, event):

        # Quit the game
        if event.type == pygame.QUIT:
            self.game_running = False

        # Resize the window
        elif event.type == VIDEORESIZE:
            self.resize(event.w, event.h)

        # Remove alerts (damages, messages)
        elif event.type == REMOVE_ALERTS:
            for a in self.alerts: a.end()

        # Modify trader's stuff
        elif event.type == RESET_TRADERS_STUFF:
            self.set_traders_stuff()

        # Create ui_manager's events
        self.inventory.ui_manager.process_events(event)
        self.market.ui_manager.process_events(event)
        self.ui_manager.process_events(event)

        # Check EventButton pressed
        if event.type == pg_gui.UI_BUTTON_START_PRESS:
            button_id = event.ui_element.object_ids[len(event.ui_element.object_ids) - 1]
            for key in self.event_buttons.keys():
                if button_id == key:
                    self.event_buttons[key].execute()

    def UI_inventory(self):

        self.dialog_box.reading = False
        scene = utils.GameScene(self)

        def script(time_delta):

            self.map_manager.draw()

            self.inventory.resize()

            if self.inventory.visible_info_zone:
                self.inventory.info_zone()

            self.inventory.update(time_delta)
            self.inventory.draw()

        def handle_events(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or pygame.K_v:
                    self.run()

        scene.launch_loop(script, handle_events)

    def UI_market(self):
        scene = utils.GameScene(self)

        def script(time_delta):
            self.map_manager.draw()

            self.market.resize()

            self.market.update(time_delta)
            self.market.draw()

        def handle_events(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or pygame.K_v:
                    self.run()

        scene.launch_loop(script, handle_events)

    def UI_died(self):
        scene = utils.GameScene(self)

        def script(time_delta):

            panel_buttons = Element(name='Panel',
                                    rect=[(-5, -5), (self.surface.get_width() + 10, self.surface.get_height() + 10)],
                                    ui_manager=self.ui_manager,
                                    object_id=Ids(_class_id='@panel', _object_id='#mainpanel').all,
                                    container=None
                                    ).UI

            resurrect_button = EventButton(rect=[(300, 450), (300, 100)],
                                          text='Ressusciter',
                                          object_id=Ids(_class_id='@button', _object_id='#resurrect_btn').all,
                                          ui_manager=self.ui_manager,
                                          container=panel_buttons,
                                          func=lambda: self.respawn()
                                          )
            self.event_buttons['#resurrect_btn'] = resurrect_button

            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.surface)

        scene.launch_loop(script)

    def UI_pause(self):
        scene = utils.GameScene(self)

        def script(time_delta): self.map_manager.draw()

        def handle_events(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or pygame.K_v:
                    self.run()

        scene.launch_loop(script, handle_events)

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
                self.w_case.blit()

                if self.player.selected_weapon:
                    self.surface.blit(self.player.selected_weapon.item_image, SELECTED_WEAPON(self.vw, self.vh))
                    self.surface.blit(utils.text(self.player.selected_weapon.munitions, None, 30, co.WHITE), MUNITION_NUMBER(self.vw, self.vh))

                if self.get_map_type() == 'dungeon':
                    self.player.set_weapon_image()
                    # Write enemies number
                    self.surface.blit(
                                    utils.text(f'{len(self.map_manager.get_map().enemys)} / {self.map_manager.current_mission.n_enemy}',
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

                self.panel_buttons = Element(name='Panel',
                                             rect=[(-5, -5),
                                                   (self.surface.get_width() + 10, self.surface.get_height() + 10)],
                                             ui_manager=self.ui_manager,
                                             object_id=Ids(_class_id='@panel', _object_id='#mainpanel').all,
                                             container=None
                                             ).UI

                self.play_btn = EventButton(
                    rect=[(100, 100), (300, 100)],
                    text=self.texts['buttons']['play'],
                    ui_manager=self.ui_manager,
                    object_id=Ids(_class_id='@button', _object_id='#play_button').all,
                    container=self.panel_buttons,
                    func=lambda: self.start()
                )
                self.event_buttons['#play_button'] = self.play_btn

                self.settings_btn = EventButton(
                    rect=[(100, 300), (300, 100)],
                    text=self.texts['buttons']['settings'],
                    ui_manager=self.ui_manager,
                    object_id=Ids(_class_id='@button', _object_id='#settings_button').all,
                    container=self.panel_buttons,
                    func=lambda: print('Paramètres')
                )
                self.event_buttons['#settings_button'] = self.settings_btn

                # Pygame Gui
                self.ui_manager.update(time_delta)
                self.ui_manager.draw_ui(self.surface)

            # Window update
            pygame.display.flip()

            # Events management
            for event in pygame.event.get():

                self.player.weapon_animation.handle_event(event)
                self.handle_events(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.attack('')
                    elif event.key == pygame.K_z:
                        self.player.attack('magic')
                    elif event.key == pygame.K_e:
                        self.player.attack('fire')
                    elif event.key == pygame.K_v:
                        self.inventory.draw_items(self.inventory.focus)
                        self.UI_inventory()
                    elif event.key == pygame.K_f:
                        self.map_manager.check_chest_collision()
                        self.map_manager.check_missioner_collision(self.dialog_box)
                        self.map_manager.check_trader_collision(self)
                    elif event.key == pygame.K_ESCAPE:
                        self.dialog_box.reading = False
                    elif event.key == pygame.K_1:
                        self.player.choice_current_weapon(0)
                    elif event.key == pygame.K_2:
                        self.player.choice_current_weapon(1)

        pygame.quit()
        sys.exit()
