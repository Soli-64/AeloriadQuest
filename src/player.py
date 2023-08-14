import json

import pygame
from src.entity import Entity
from src.Weapons.weapon import Weapon
from src.Weapons.magic_weapon import MagicWeapon
import src.Utils.pygame_functions as f_pg


class Player(Entity):

    x = 100
    y = 100

    def __init__(self, game):
        super().__init__("player", './assets/images/sprite/player.png', self.x, self.y)
        self.game = game
        self.reach = 15
        self.speed = 5
        self.level = 1
        self.max_health = 400
        self.health = 400
        self.damage = 10
        self.money = 0
        self.weapons = []
        self.currents_weapons = []
        self.selected_weapon = None
        self.xp = 0
        self.munition = {
            "normal": 20,
            "petites": 20,
            "grandes": 10,
            "lourdes": 5,
            "explosives": 2,
            "none": "infinite"
        }

    def get_json(self):
        with open('./assets/json/player/level.json', 'r+') as file:
            data = json.load(file)
            self.level = data['1']

    def choice_current_weapon(self, index):
        self.selected_weapon = self.currents_weapons[index]
        self.damage = self.selected_weapon.damage

    def select_weapons(self, indexs):
        for x in range(0, len(indexs)):
            if self.currents_weapons and len(self.currents_weapons) < 3:
                self.currents_weapons.append(self.weapons[indexs[x]])
            else:
                self.currents_weapons.append(self.weapons[indexs[x]])

    def add_weapons(self, weapons):
        for w in weapons:
            self.weapons.append(w)
        self.select_weapons([0, 1])

    def isEnemy(self): return False

    def add_money(self, amount): self.money += amount

    def apply_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.game.died()

    def remove_money(self, amount):
        if self.money - amount >= 0:
            self.money -= amount
        else:
            self.money = 0

    def update_stats(self, surface):
        # health_barre
        pygame.draw.rect(surface, (60, 63, 60), [150, 35, self.max_health, 16])
        pygame.draw.rect(surface, (111, 210, 46), [150, 35, self.health, 16])
        # money
        surface.blit(f_pg.text(self.money, None, 50), (self.game.vw - 165, 35))

    def attack(self, type):
        if self.selected_weapon:
            if type == 'magic':
                self.selected_weapon.magic_attack()
            elif type == 'fire':
                self.selected_weapon.fire_attack()
            else:
                self.selected_weapon.attack()
        else:
            print('selectionne une arme pour attaquer !')
