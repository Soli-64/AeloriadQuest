import random, json
import pygame
from src.Enemy.enemy import Enemy

class Mission:

    def __init__(self, map_manager, level, rewards, missioner):
        self.level = level
        self.rewards = rewards
        self.map_manager = map_manager
        self.map_name = 'default map name'
        self.set_map_name()
        self.n_enemy = self.level * 1
        self.missioner = missioner
        self.set_mission()
        self.isFinished = False

    def set_map_name(self):
        with open('./assets/json/maps.json', 'r') as file:
            data = json.load(file)
            self.map_name = random.choice(data['dungeons'])

    def set_mission(self):
        teleporters = []
        enemys = []
        for x in range(0, self.n_enemy):
            enemys.append(
                Enemy(self.map_manager.player, self.map_manager)
            )
        self.map_manager.register_map(name=self.map_name, teleporters=teleporters, enemys=enemys, missioners=[], items=[], projectils=[], traders=[])

    def activ_mission(self):
        self.map_manager.current_map = self.map_name
        self.map_manager.teleport_player("player")

    def check_finished_mission(self):
        if len(self.map_manager.get_map().enemys) <= 0:
            self.map_manager.get_map().teleporters.append(
                self.map_manager.get_teleporter(self.map_name, 'exit', 'world', 'end_mission')
            )
            point = self.map_manager.get_object('chest')
            chest = self.map_manager.get_chest(point.x, point.y)
            self.map_manager.get_map().items.append(chest)
            self.map_manager.get_map().group.add(chest)
            self.isFinished = True

    def update(self):
        pygame.draw.rect(self.map_manager.screen, (60, 63, 60), [150, 35, 100, 16])
        pygame.draw.rect(self.map_manager.screen, (111, 210, 46), [150, 35, 100, 16])