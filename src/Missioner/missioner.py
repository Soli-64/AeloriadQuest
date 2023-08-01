import pygame
from src.entity import Entity
from src.Missioner.mission import Mission

class Missioner(Entity):

    x = 300
    y = 300

    def __init__(self, name, position, map_manager):
        super().__init__("missioners/robin", self.x, self.y)
        self.name = name
        self.position = position
        self.mission = Mission(map_manager, 1, 100, "dungeon2")

    def launch_mission(self):
        self.mission.activ_mission()
