import pygame
import src.Utils.pygame_functions as f_pg
from src.Utils.settings import *

class Market:

    def __init__(self, map_manager, trader):
        self.map_manager = map_manager
        self.trader = trader
        self.game = map_manager.game
        self.image = f_pg.pygame_image('./assets/images/interfaces/market/market.png', [self.game.vw / 1.3, self.game.vh])
        self.buy_btn = f_pg.pygame_image('./assets/images/interfaces/market/buy_btn.png', [300, 100])
        self.sell_btn = f_pg.pygame_image('./assets/images/interfaces/market/sell_btn.png', [300, 100])

    def blit(self):
        size = MARKET(self.game.vw, self.game.vh)
        self.game.surface.blit(self.image, (size[0], size[1]))
