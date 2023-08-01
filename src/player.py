import pygame
from src.entity import Entity


class Player(Entity):

    x = 100
    y = 100

    def __init__(self, game):
        super().__init__("player", self.x, self.y)
        self.game = game
        self.reach = 30
        self.speed = 3
        self.interface_max_health = 200
        self.max_health = 370
        self.health = 350
        self.damage = 10
        self.money = 0
        self.weapons = []
        self.currents_weapons = [self.weapons[0], self.weapons[1], self.weapons[2]]
        self.selected_weapon = self.currents_weapons [0]

    def add_weapons(self, weapons):
        for w in weapons:
            self.weapons.append(w)

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


        # dessiner notre barre de vie


    def attack(self):
        for enemy in self.game.map_manager.get_map().enemys:
            knock_stats = self.localize(enemy, self.reach)
            print(knock_stats)
            if knock_stats:
                enemy.health -= self.damage
                if enemy.health <= 0:
                    enemy.remove()
