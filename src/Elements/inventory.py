import pygame, pygame_gui as pg_gui
from src.Elements.element import *


class Inventory(ParentElement):

    def __init__(self, screen: pygame.Surface, player):
        super().__init__(screen, './assets/json/graffics/inventory/style.json')
        self.player = player
        self.items = player.inventory

        self.focus = "weapon"

        self.panel = None
        self.info_panel = None
        self.weapon_panel = None
        self.weapons_label = None

        self.sub_info_panel = None
        self.index = None

        self.elements = {}
        self.buttons = []
        self.elements_weapons = []

        self.resize(screen)
        self.draw_items(self.focus)

    def set_focus(self, _focus): self.focus = _focus

    def draw_items(self, _item):

        inter_x, inter_y = 10, 20
        x_index, y_index = 20, 60
        case_index, index = 0, 0
        self.line_case = round((self.screen.get_size()[0] - 525) / (50 + inter_x)) - 1

        if _item == "weapon":

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

                button = IndexButton(
                                rect=[(0, 0), (50, 50)],
                                ui_manager=self.ui_manager,
                                text= '',
                                object_id= Ids('@case_button', f'#weapon{index}').all,
                                container=panel,
                                inventory=self
                                )

                self.buttons.append(button)
                self.elements[f'w{index}'] = i
                x_index += (inter_x + 50)
                case_index += 1
                index += 1

        elif _item == "objects":
            print('object page')

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

        self.info_panel = Element(name='Panel',
                                  rect=[(self.screen.get_size()[0] - 500, -3), (350, self.screen.get_size()[1] - 200)],
                                  ui_manager=self.ui_manager,
                                  object_id='@panel',
                                  container=self.panel
                                  ).UI

        self.weapon_panel = Element(name='Panel',
                                    rect=[(-2, -2), (self.screen.get_size()[0] - 500, 200)],
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

    def set_index(self, _button):
        self.index = int(self.buttons.index(_button))

    def info_zone(self):

        target_element = self.elements[f'w{self.index}']

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

