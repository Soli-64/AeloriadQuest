import pygame, pytmx, pyscroll
from src.game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()