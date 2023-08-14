from src.entity import Entity
from random import randint
import pygame

class Enemy(Entity):

    x = 200
    y = 200

    def __init__(self, player, map_manager):
        super().__init__("enemy", './assets/images/sprite/enemys/enemy.png', self.x, self.y)
        self.player = player
        self.map_manager = map_manager
        self.set_enemy_animation()
        self.speed = randint(1, 3)
        self.max_health = 50
        self.health = 50
        self.damage = 1
        self.teleport(randint(200, 2000), randint(50, 2000))
        self.direction = 'x'

    def apply_damage(self, amount):
        self.animations('damaged')
        self.health -= amount
        if self.health <= 0:
            self.remove()

    def modifyDirection(self):
        if self.direction == 'x':
            self.direction = 'y'
        else:
            self.direction = 'x'

    def isEnemy(self):
        return True

    def teleport(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def move(self):
        if self.localize(self.player, 200):
            if self.direction == 'x':
                self.move_X()
            else:
                self.move_Y()

    def move_Y(self):
        if (self.localize(self.player, 20)):
            self.attack()
        else:
            if self.player.rect.y > self.rect.y + 10:
                self.move_right()
            elif self.player.rect.y < self.rect.y - 10:
                self.move_left()
            else:
                if self.player.rect.x > self.rect.x + 10:
                    self.move_down()
                elif self.player.rect.x < self.rect.x - 10:
                    self.move_up()

    def move_X(self):
        if (self.localize(self.player, 20)):
            self.attack()
        else:
            if self.player.rect.x > self.rect.x + 10:
                self.move_right()
            elif self.player.rect.x < self.rect.x - 10:
                self.move_left()
            else:
                if self.player.rect.y > self.rect.y + 10:
                    self.move_down()
                elif self.player.rect.y < self.rect.y - 10:
                    self.move_up()

    def attack(self):
        if self.localize(self.player, 20):
            self.player.apply_damage(self.damage)

    def remove(self):
        self.player.add_money(randint(0, 2))
        self.map_manager.get_map().enemys.remove(self)
        self.map_manager.current_mission.check_finished_mission()
        self.kill()
