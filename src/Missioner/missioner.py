import pygame, random, json
from src.entity import Entity
from src.Missioner.mission import Mission

class Missioner(Entity):

    x = 300
    y = 300

    def __init__(self, name, position, map_manager):
        super().__init__(f"missioners/{name}", self.x, self.y)
        self.name = name
        self.position = position
        self.level = round(map_manager.player.level / 2) + 1
        self.mission = Mission(map_manager, self.level, self.level*100, "dungeon2")
        self.dialog = []
        self.choose_texts()

    def choose_texts(self):
        with open('./assets/json/texts/missioner_texts.json', 'r+', 1, 'utf8', None, "\r\n") as file:
            data = json.load(file)
            for x in range(1, 5):
                text = random.choice(data[f'sentence{x}'])
                self.dialog.append(text)

    def present_mission(self):
        print('Voici votre mission:')

    def launch_mission(self):
        self.mission.activ_mission()
