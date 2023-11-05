import pygame, pygame_gui as pg_gui
from src.Elements.element import *
from src.Weapons.weapon import Weapon
from src.Weapons.magic_weapon import MagicWeapon
from src.Weapons.FireWeapon.fire_weapon import FireWeapon

class InventoryButton(Button):

    def __init__(self, rect, text, ui_manager, object_id, container, inv):
        super().__init__(rect, text, ui_manager, object_id, container)
        self.inv = inv
    def execute(self):
        self.inv.visible_info_zone = True
        self.inv.pressed_button_id = self.object_id.object_id

class Inventory(ParentElement):

    def __init__(self, game,  screen: pygame.Surface, player):
        super().__init__(screen, './assets/json/graffics/inventory/style.json')

        self.game = game
        self.screen = screen

        self.player = player
        self.items = player.inventory

        self.focus = "weapons"

        #self.panel = None
        self.panel, self.info_panel = [None] * 2

        self.tab_panel = None
        self.weapon_tab_button, self.objects_tab_button = [None] * 2

        self.weapon_panel, self.weapons_label = [None] * 2

        self.charger_panel = None

        self.sub_info_panel = None

        self.visible_info_zone = False
        self.pressed_button_id = None

        self.elements = {}
        self.event_buttons = {}
        self.buttons = []
        self.elements_weapons = []

        self.resize()
        self.draw_items(self.focus)

    def set_btn_id(self, _id):
        self.visible_info_zone = True
        self.pressed_button_id = _id

    def set_focus(self, focus):
        self.visible_info_zone = False
        if self.info_panel is not None: self.info_panel.kill()
        self.pressed_button_id = None
        self.focus = focus

    def draw_items(self, item):

        self.elements = {}
        self.buttons = []

        inter_x, inter_y = 10, 20
        x_index, y_index = 20, 60
        case_index, index = 0, 0
        self.line_case = round((self.screen.get_size()[0] - 525) / (50 + inter_x))

        self.index = None
        index = 0

        self.items_panel = Element(name='Panel',
                                        rect=[(-2, 50), (self.screen.get_size()[0] - 500, self.screen.get_size()[1] - 250)],
                                        ui_manager=self.ui_manager,
                                        object_id=Ids(_class_id='@weapon_panel', _object_id='#').all,
                                        container=self.panel
                                        ).UI

        self.items_label = TextElement(name='Label',
                                         rect=[(20, 10), (500, 50)],
                                         text=f'{item}',
                                         ui_manager=self.ui_manager,
                                         object_id=Ids(_class_id='@label', _object_id='#').all,
                                         container=self.items_panel
                                         ).UI

        for i in self.items[item]:

            if case_index >= self.line_case:
                y_index += inter_y + 50
                x_index = 20
                case_index = 0

            panel = Element(name='Panel',
                            rect=[(x_index, y_index), (50, 50)],
                            ui_manager=self.ui_manager,
                            object_id=None,
                            container=self.items_panel
                            ).UI

            image = ImageElement(rect=[(2, 2), (40, 40)],
                                 img= i.item_image,
                                 ui_manager=self.ui_manager,
                                 object_id=None,
                                 container=panel
                                 ).UI

            button = InventoryButton(
                rect=[(0, 0), (50, 50)],
                ui_manager=self.ui_manager,
                text="",
                object_id=Ids('@case_button', f'#{item}{index}').all,
                container=panel,
                inv=self
            )
            self.game.event_buttons[f'#{item}{index}'] = button

            self.elements[f'#{item}{index}'] = i
            x_index += (inter_x + 50)
            case_index += 1
            index += 1

    def resize(self):

        self.set_manager(self.screen, './assets/json/graffics/inventory/style.json')

        self.panel = Element(name='Panel',
                             rect=[(120, 100), (self.screen.get_size()[0] - 150, self.screen.get_size()[1] - 200)],
                             ui_manager=self.ui_manager,
                             object_id=Ids(_class_id='@inventory', _object_id='#').all,
                             container=None
                             ).UI

        self.tab_panel = Element(name='Panel',
                                 rect=[(-2, -2), (self.screen.get_size()[0] - 500, 50)],
                                 ui_manager=self.ui_manager,
                                 object_id=Ids(_class_id='@panel', _object_id='#').all,
                                 container=self.panel
                                 ).UI

        self.weapon_tab_button = EventButton(
                                            rect=[(0, 0), (100, 50)],
                                            text="Armes",
                                            ui_manager=self.ui_manager,
                                            object_id=Ids(_class_id='@', _object_id='#weapon_tab_button').all,
                                            container=self.tab_panel,
                                            func= lambda : self.set_focus("weapons")
                                            )
        self.game.event_buttons['#weapon_tab_button'] = self.weapon_tab_button

        self.charger_tab_button = EventButton(
                                            rect=[(100, 0), (100, 50)],
                                            text="Objets",
                                            ui_manager=self.ui_manager,
                                            object_id=Ids(_class_id='@', _object_id='#charger_tab_button').all,
                                            container=self.tab_panel,
                                            func= lambda: self.set_focus("chargers")
                                            )
        self.game.event_buttons['#charger_tab_button'] = self.charger_tab_button

        self.info_panel = Element(name='Panel',
                                  rect=[(self.screen.get_size()[0] - 500, -3), (350, self.screen.get_size()[1] - 200)],
                                  ui_manager=self.ui_manager,
                                  object_id=Ids(_class_id='@panel', _object_id='#').all,
                                  container=self.panel
                                  ).UI

        self.draw_items(self.focus)

    def info_zone(self):

        target_element = self.elements[f'{self.pressed_button_id}']


        if self.sub_info_panel is not None:
            self.sub_info_panel.kill()

        self.sub_info_panel = Element(name='Panel',
                                      rect=[(0, 0), (350, self.screen.get_size()[1] - 200)],
                                      ui_manager=self.ui_manager,
                                      object_id= Ids(_class_id='@v_panel', _object_id='#sub_info_panel').all, # No Ids('@v_panel', '#sub_info_panel').all,
                                      container=self.info_panel
                                      ).UI

        image = ImageElement(rect=[(70, 0), (200, 200)],
                             img=target_element.item_image,
                             ui_manager=self.ui_manager,
                             object_id=Ids(_class_id='@', _object_id='#').all,
                             container=self.sub_info_panel
                             )

        sub_panel = Element(name='Panel',
                            rect=[(-5, 200), (350, self.screen.get_size()[1] - 410)],
                            ui_manager=self.ui_manager,
                            object_id= Ids(_class_id='@', _object_id='#sub_panel').all, # No Ids('@a', '#sub_info_label').all,
                            container=self.sub_info_panel
                            ).UI

        if type(target_element) is Weapon:

            damage_label = TextElement(
                                    name='Label',
                                    rect=[(0, 0), (350, 50)],
                                    text=f'Dégats: {target_element.damage}',
                                    ui_manager=self.ui_manager,
                                    object_id=Ids(_class_id='@info_label', _object_id='#').all,
                                    container=sub_panel
            ).UI
