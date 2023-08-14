import pygame
from src.entity import Entity


class Traider(Entity):

    x = 350
    y = 300

    def __init__(self, name, position, map_manager):
        super().__init__(name, f'./assets/images/sprite/traiders/{name}.png', self.x, self.y)
        self.name = name
        self.position = position
        self.map_manager = map_manager
        self.marchandise = {

        }