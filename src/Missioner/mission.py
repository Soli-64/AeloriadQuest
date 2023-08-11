import pygame
from src.Enemy.enemy import Enemy
from src.Items.chest import Chest

class Mission:

    def __init__(self, map_manager, level, rewards, map_name):
        self.level = level
        self.rewards = rewards
        self.map_manager = map_manager
        self.map_name = map_name
        self.set_mission()

    def set_mission(self):
        teleporters = []
        enemys = []
        for x in range(0, self.level * 10):
            enemys.append(
                Enemy(self.map_manager.player, self.map_manager)
            )
        self.map_manager.register_map(name=self.map_name, teleporters=teleporters, npcs=[], enemys=enemys, missioners=[], items=[])

    def activ_mission(self):
        self.map_manager.current_map = self.map_name
        self.map_manager.teleport_player("player")


    def check_finished_mission(self):
        if not len(self.map_manager.get_map().enemys) > 0:
            self.map_manager.get_map().teleporters.append(
                self.map_manager.get_teleporter(self.map_name, 'exit', 'world', 'player')
            )
            point = self.map_manager.get_object('chest')

            self.map_manager.get_map().items.append(self.map_manager.get_chest(point.x, point.y))
            self.map_manager.get_map().group.add(self.map_manager.get_chest(point.x, point.y))

    def update(self):
        pygame.draw.rect(self.map_manager.screen, (60, 63, 60), [150, 35, 100, 16])
        pygame.draw.rect(self.map_manager.screen, (111, 210, 46), [150, 35, 100, 16])