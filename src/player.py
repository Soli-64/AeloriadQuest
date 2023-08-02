import pygame
from src.entity import Entity
from src.Weapons.weapon import Weapon
from src.Weapons.fire_weapon import FireWeapon
from src.Weapons.projectile import Projectile


class Player(Entity):

    x = 100
    y = 100

    def __init__(self, game):
        super().__init__("player", self.x, self.y)
        self.game = game
        self.reach = 15
        self.speed = 3
        self.interface_max_health = 200
        self.max_health = 370
        self.health = 350
        self.damage = 10
        self.money = 0
        self.projectiles = []
        self.weapons = []
        self.currents_weapons = []
        self.selected_weapon = False
        #self.selected_weapon = self.currents_weapons[0]

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

    def isEnemy(self):
        return False

    def add_money(self, amount):
        self.money += amount

    def remove_money(self, amount):
        if self.money - amount >= 0:
            self.money -= amount
        else:
            self.money = 0

    def update_health_bar(self, surface):
        if self.max_health <= 200:
            pygame.draw.rect(surface, (60, 63, 60), [52, 148, 185, 16])
            pygame.draw.rect(surface, (111, 210, 46), [52, 148, self.health, 16])
        else :
            if (self.health > 200):
                # Première barre
                pygame.draw.rect(surface, (60, 63, 60), [52, 148, 185, 16])
                pygame.draw.rect(surface, (111, 210, 46), [52, 148, 185, 16])
                # Seconde barre
                pygame.draw.rect(surface, (60, 63, 60), [52, 187, 185, 16])
                pygame.draw.rect(surface, (111, 210, 46), [52, 187, self.health - 185, 16])
            else:
                # Première barre
                pygame.draw.rect(surface, (60, 63, 60), [52, 148, 185, 16])
                pygame.draw.rect(surface, (111, 210, 46), [52, 148, self.health, 16])
                # Seconde barre
                pygame.draw.rect(surface, (60, 63, 60), [52, 187, 185, 16])
                pygame.draw.rect(surface, (111, 210, 46), [52, 187, 0, 16])

    def apply_damage(self, amount):
        self.health -= amount

    def attack(self):
        if self.selected_weapon:
            if type(self.selected_weapon) is FireWeapon: self.selected_weapon.fire_attack()
            else: self.selected_weapon.attack()
        else:
            print('selectionne une arme pour attaquer !')