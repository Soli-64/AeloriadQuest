import pygame, random
from src.entity import Entity
from src.Weapons.weapon import Weapon
from src.Weapons.FireWeapon.fire_weapon import FireWeapon


class Trader(Entity):

    x = 350
    y = 300

    def __init__(self, name, position, map_manager):
        super().__init__(name, f'./assets/images/sprite/traders/{name}.png', self.x, self.y)
        self.name = name
        self.position = position
        self.map_manager = map_manager

        self.weapons_names = ['sword']
        self.fireweapons_names = ['gun']

        self.stock = {
            "weapons": [],
            "objects": []
        }

    def new_random_weapon(self):
        weapon_type = random.randint(0, 1)
        if weapon_type == 0:
            w_name = random.choice(self.weapons_names)
            return Weapon(w_name, 1, self.map_manager)
        elif weapon_type == 1:
            w_name = random.choice(self.fireweapons_names)
            return FireWeapon(w_name, 1, self.map_manager)

    def create_random_stuff(self):
        self.stock['weapons'] = []
        for x in range(0, 3):
            self.stock['weapons'].append(
                self.new_random_weapon()
            )
