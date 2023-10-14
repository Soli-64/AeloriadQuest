import pygame, pygame_gui as pg_gui, json
from src.Elements.element import *
from src.Weapons.weapon import Weapon
from src.Weapons.magic_weapon import MagicWeapon
from src.Weapons.FireWeapon.fire_weapon import FireWeapon


class Market(ParentElement):

    def __init__(self, game,  screen: pygame.Surface, player):
        super().__init__(screen, './assets/json/graffics/inventory/style.json')
        self.player = player

        self.game = game

        self.focus = 'weapon'

        self.stock = {
            "weapons": [],
            "objects": []
        }

        self.get_prices()
        self.resize(screen)

    def set_focus(self, focus):
        self.focus = focus

    def sell_item(self, price, item_type, item, id):
        if self.player.money >= price:
            self.player.remove_money(price)
            self.player.add_weapons([item])
            self.stock['weapons'].pop(id)
            self.resize(self.screen)

    def get_prices(self):
        with open('./assets/json/items/price.json', 'r') as file:
            self.prices = json.load((file))

    def new_article(self, pos, container, item, index, id):
        panel = Element(name='Panel',
                        rect=[(pos[0], pos[1]), (100, 200)],
                        ui_manager=self.ui_manager,
                        object_id='@article',
                        container=container
                        ).UI
        image = ImageElement(rect=[(0, 5), (90, 90)],
                             img=item.item_image,
                             ui_manager=self.ui_manager,
                             object_id='@item_img',
                             container=panel
                             ).UI
        button = EventButton(rect=[(0, 150), (90, 40)],
                             text='Acheter',
                             ui_manager=self.ui_manager,
                             object_id=f'#buy_button{index}',
                             container=panel,
                             func=lambda: self.sell_item(self.prices[item.name][0], 'weapon', item, id)
                             )
        self.game.event_buttons[f'#buy_button{index}'] = button

    def resize(self, screen):

        self.set_manager(screen, './assets/json/graffics/market/style.json')
        self.screen = screen

        self.panel = Element(name='Panel',
                             rect=[(100, 70), (self.screen.get_size()[0] - 200, self.screen.get_size()[1] - 150)],
                             ui_manager=self.ui_manager,
                             object_id='@market',
                             container=None
                             ).UI

        self.tab_panel = TabPanel(ui_manager=self.ui_manager,
                                  rect=[(0, 0), (self.screen.get_size()[0] - 200, 60)],
                                  object_id='@tab_panel',
                                  container=self.panel
                                  ).UI

        self.tab_weapon = EventButton(rect=[(0, 0), (120, 60)],
                                     text='Armes',
                                     ui_manager=self.ui_manager,
                                     object_id='@tab_button',
                                     container=self.tab_panel,
                                     func= lambda: self.set_focus('weapon')
                                     )

        self.tab_objects = EventButton(rect=[(120, 0), (120, 60)],
                                         text='Objets',
                                         ui_manager=self.ui_manager,
                                         object_id=Ids(_class_id='@tab_panel', _object_id='#market_object_tab'),
                                         container=self.tab_panel,
                                         func=lambda: self.set_focus('object')
                                         )
        self.game.event_buttons['#market_object_tab'] = self.tab_objects

        self.shop_zone = Element(name='Panel',
                                 rect=[(0, 60), (self.screen.get_size()[0] - (self.screen.get_size()[0] / 2), self.screen.get_size()[1] - 195)],
                                 ui_manager=self.ui_manager,
                                 object_id="#shop_zone",
                                 container=self.panel
                                 ).UI

        self.articles = Element(name='Panel',
                                rect=[(0, 40), (self.screen.get_size()[0] - (self.screen.get_size()[0] / 2), self.screen.get_size()[1] - 270)],
                                ui_manager=self.ui_manager,
                                object_id='@articles',
                                container=self.shop_zone
                                ).UI

        line_width = self.screen.get_size()[0] - (self.screen.get_size()[0] / 2)
        article_by_line = int(line_width / 110)
        line_index = 0
        column_index = 0
        position = [5, 5]
        index = 0

        for item in self.stock['weapons']:
            if line_index >= article_by_line - 1:
                column_index += 1
                position[1] += 210
                position[0] = 5
                self.new_article(position, self.articles, item, index, index)
            else:
                position[0] += 110
                line_index += 1
                self.new_article(position, self.articles, item, index, index)
                index += 1
