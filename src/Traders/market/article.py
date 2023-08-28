import pygame, json
import src.Utils.pygame_functions as f_pg

class Article:

    def __init__(self, map_manager, market, item):
        self.map_manager = map_manager
        self.market = market
        self.item = item
        self.type = item.type
        self.price = 'default price'
        self.set_item_stats()
        self.image = f_pg.pygame_image('./assets/images/interfaces/market/article/png', [320, 320])
        self.buy_btn = f_pg.pygame_image('./assets/images/interfaces/market/buy_btn.png', [300, 100])
        self.sell_btn = f_pg.pygame_image('./assets/images/interfaces/market/sell_btn.png', [300, 100])

    def set_item_stats(self):
        with open('./assets/json/market/price.json', 'r') as price:
            data = json.load(price)
            self.price = data[self.item.name]

    def player_buy(self):
        self.map_manager.player.remove_money(self.price)
        self.map_manager.player.inventory[self.type].append(self.item)
        self.market.stock.remove(self)