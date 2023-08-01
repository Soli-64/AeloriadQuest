import pygame
from random import randint
from src.Enemy.enemy import Enemy


class Mission:

    def __init__(self, map_manager, level, rewards, map_name):
        self.level = level
        self.rewards = rewards
        self.map_manager = map_manager
        self.map = map_name
        self.set_mission()

    def set_mission(self):
        teleporters = []
        enemys = []
        for x in range(0, self.level * 10):
            enemys.append(
                Enemy(self.map_manager.player, self.map_manager)
            )
        self.map_manager.register_map(name=self.map, teleporters=teleporters, npcs=[], enemys=enemys, missioners=[])

    def activ_mission(self):
        self.map_manager.current_map = self.map

    def finished_mission(self):
        self.map_manager.current_map = "carte"