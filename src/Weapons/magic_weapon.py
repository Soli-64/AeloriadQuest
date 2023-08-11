from src.Weapons.weapon import Weapon


class MagicWeapon(Weapon):

    def __init__(self, name, level, map_manager, player):
        super().__init__(name, level, map_manager, player)
        self.name = name
        self.level = level
        self.map_manager = map_manager
        self.player = player

    def magic_attack(self):
        pass
