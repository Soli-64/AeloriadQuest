import pygame, pygame_gui as pg_gui
from src.Elements.element import *
from src.Weapons.weapon import Weapon
from src.Weapons.magic_weapon import MagicWeapon
from src.Weapons.FireWeapon.fire_weapon import FireWeapon

class InventoryButton(Button):

    def __init__(self, _rect, _text, _ui_manager, _object_id, _container, _inv):
        super().__init__(_rect, _text, _ui_manager, _object_id, _container)
        self.inv = _inv
    def execute(self):
        self.inv.visible_info_zone = True
        self.inv.pressed_button_id = self.object_id.object_id

class Inventory(ParentElement):

    def __init__(self, game,  screen: pygame.Surface, player):
        super().__init__(screen, './assets/json/graffics/inventory/style.json')

        self.game = game

        self.player = player
        self.items = player.inventory

        self.focus = "weapons"

        #self.panel = None
        self.panel, self.info_panel = [None] * 2

        self.tab_panel = None
        self.weapon_tab_button, self.objects_tab_button = [None] * 2

        self.weapon_panel, self.weapons_label = [None] * 2

        self.sub_info_panel = None

        self.visible_info_zone = False
        self.pressed_button_id = None

        self.elements = {}
        self.event_buttons = {}
        self.buttons = []
        self.elements_weapons = []

        self.resize(screen)
        self.draw_items(self.focus)

    def set_btn_id(self, _id):
        self.visible_info_zone = True
        self.pressed_button_id = _id

    def set_focus(self, _focus):
        self.visible_info_zone = False
        if self.info_panel is not None: self.info_panel.kill()
        self.pressed_button_id = None
        self.focus = _focus
        self.draw_items(self.focus)

    def draw_items(self, _item):

        if self.weapon_panel:
            self.weapon_panel.kill()

        self.elements = {}
        self.buttons = []

        inter_x, inter_y = 10, 20
        x_index, y_index = 20, 60
        case_index, index = 0, 0
        self.line_case = round((self.screen.get_size()[0] - 525) / (50 + inter_x)) - 1

        if _item == "weapons":

            self.index = None
            index = 0

            self.weapon_panel = Element(name='Panel',
                                        rect=[(-2, 50), (self.screen.get_size()[0] - 500, self.screen.get_size()[1] - 250)],
                                        ui_manager=self.ui_manager,
                                        object_id='@weapon_panel',
                                        container=self.panel
                                        ).UI

            self.weapons_label = TextElement(name='Label',
                                             rect=[(20, 10), (500, 50)],
                                             text='ARMES',
                                             ui_manager=self.ui_manager,
                                             object_id='@label',
                                             container=self.weapon_panel
                                             ).UI

            for i in self.items['weapons']:

                if case_index >= self.line_case:
                    y_index += inter_y + 50
                    x_index = 20
                    case_index = 0

                panel = Element(name='Panel',
                                rect=[(x_index, y_index), (50, 50)],
                                ui_manager=self.ui_manager,
                                object_id='',
                                container=self.weapon_panel
                                ).UI

                image = ImageElement(rect=[(2, 2), (45, 45)],
                                     img= i.item_image,
                                     ui_manager=self.ui_manager,
                                     object_id='',
                                     container=panel
                                     ).UI

                button = InventoryButton(
                    _rect=[(0, 0), (50, 50)],
                    _ui_manager=self.ui_manager,
                    _text="",
                    _object_id=Ids('@case_button', f'#weapon{index}').all,
                    _container=panel,
                    _inv=self
                )
                self.game.event_buttons[f'#weapon{index}'] = button
                #self.event_buttons[f'#weapon{index}'] = button

                self.elements[f'#weapon{index}'] = i
                x_index += (inter_x + 50)
                case_index += 1
                index += 1

        elif _item == "objects":
            self.index = None

    def resize(self, _screen):

        self.set_manager(_screen, './assets/json/graffics/inventory/style.json')
        self.screen = _screen

        if self.panel is not None:
            self.panel.kill()

        self.panel = Element(name='Panel',
                             rect=[(120, 100), (self.screen.get_size()[0] - 150, self.screen.get_size()[1] - 200)],
                             ui_manager=self.ui_manager,
                             object_id='@inventory',
                             container=None
                             ).UI

        self.tab_panel = Element(name='Panel',
                                 rect=[(-2, -2), (self.screen.get_size()[0] - 500, 50)],
                                 ui_manager=self.ui_manager,
                                 object_id='@panel',
                                 container=self.panel
                                 ).UI

        self.weapon_tab_button = EventButton(
                                            rect=[(0, 0), (100, 50)],
                                            text="Armes",
                                            ui_manager=self.ui_manager,
                                            object_id='#weapon_tab_button',
                                            container=self.tab_panel,
                                            func= lambda : self.set_focus("weapons")
                                            )
        self.game.event_buttons['#weapon_tab_button'] = self.weapon_tab_button

        self.objects_tab_button = EventButton(
                                            rect=[(100, 0), (100, 50)],
                                            text="Objets",
                                            ui_manager=self.ui_manager,
                                            object_id='#object_tab_button',
                                            container=self.tab_panel,
                                            func= lambda: self.set_focus("objects")
                                            )
        self.game.event_buttons['#object_tab_button'] = self.objects_tab_button


        self.info_panel = Element(name='Panel',
                                  rect=[(self.screen.get_size()[0] - 500, -3), (350, self.screen.get_size()[1] - 200)],
                                  ui_manager=self.ui_manager,
                                  object_id='@panel',
                                  container=self.panel
                                  ).UI

    def info_zone(self):

        target_element = self.elements[f'{self.pressed_button_id}']

        if self.sub_info_panel is not None:
            self.sub_info_panel.kill()

        self.sub_info_panel = Element(name='Panel',
                                      rect=[(0, 0), (350, self.screen.get_size()[1] - 200)],
                                      ui_manager=self.ui_manager,
                                      object_id= '#sub_info_panel', # No Ids('@v_panel', '#sub_info_panel').all,
                                      container=self.info_panel
                                      ).UI

        image = ImageElement(rect=[(70, 0), (200, 200)],
                             img=target_element.item_image,
                             ui_manager=self.ui_manager,
                             object_id='',
                             container=self.sub_info_panel
                             )

        sub_panel = Element(name='Panel',
                            rect=[(-5, 200), (350, self.screen.get_size()[1] - 410)],
                            ui_manager=self.ui_manager,
                            object_id= '#sub_panel', # No Ids('@a', '#sub_info_label').all,
                            container=self.sub_info_panel
                            ).UI

        if type(target_element) is Weapon:

            damage_label = TextElement(
                                    name='Label',
                                    rect=[(0, 0), (350, 50)],
                                    text=f'Dégats: {target_element.damage}',
                                    ui_manager=self.ui_manager,
                                    object_id='@info_label',
                                    container=sub_panel
            ).UI
