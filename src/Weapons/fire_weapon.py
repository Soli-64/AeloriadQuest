from src.Weapons.weapon import Weapon
from src.Weapons.projectile import Projectile


class FireWeapon(Weapon):

    def __init__(self, name, level, map_manager, player):
        super().__init__(name, level, map_manager, player)
        self.name = name
        self.level = level
        self.map_manager = map_manager
        self.player = player

    def fire_attack(self):
        print('fire attack')
        p = Projectile('projectile', self.map_manager, self.player, self.player.position[0], self.player.position[1])
        self.player.projectiles.append(p)
