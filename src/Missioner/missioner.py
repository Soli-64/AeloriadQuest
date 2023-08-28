import pygame, random, json
from src.entity import Entity
from src.Missioner.mission import Mission

class Missioner(Entity):

    x = 300
    y = 300

    def __init__(self, name, map_manager):
        super().__init__(name, f'./assets/images/sprite/missioners/{name}.png',  self.x, self.y)
        self.map_manager = map_manager
        self.name = name
        self.position = self.choose_position()
        self.level = round(map_manager.player.level / 2) + 1
        self.mission = Mission(self.map_manager, self.level, self.level*50, self)
        self.dialog = []
        self.choose_texts('mission')

    def end_mission(self):
        self.map_manager.player.add_money(self.mission.rewards)
        self.map_manager.current_mission = None
        missioner = self.map_manager.get_missioner()
        self.map_manager.get_group().add(missioner)
        self.map_manager.get_map().missioners.append(missioner)
        self.remove()

    def remove(self):
        self.map_manager.get_group().remove(self)
        self.map_manager.get_map().missioners.remove(self)

    def choose_position(self):
        with open('./assets/json/missioners/missioner.json', 'r+', 1, 'utf8', None, "\r\n") as file:
            data = json.load(file)
            temp = True
            while temp:
                pos = random.choice(data['positions'])
                if not pos in self.map_manager.game.missioners_occupied_position:
                    temp = False
            print(pos)
            self.map_manager.game.missioners_occupied_position.append(pos)
            return pos

    def choose_texts(self, typetext):
        self.dialog = []
        with open('./assets/json/missioners/missioner.json', 'r+', 1, 'utf8', None, "\r\n") as file:
            data = json.load(file)
            for x in range(1, len(data['texts']['fr'][typetext] ) + 1):
                text = random.choice(data['texts']['fr'][typetext][f'sentence{x}'])
                self.dialog.append(text)

    def present_mission(self):
        pass

    def launch_mission(self):
        self.mission.activ_mission()
        return self.mission
