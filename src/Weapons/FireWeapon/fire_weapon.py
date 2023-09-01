from src.Weapons.weapon import Weapon
from src.Weapons.projectil import Projectil


class FireWeapon(Weapon):

    def __init__(self, name, level, map_manager, player, animation_path):
        super().__init__(name, level, map_manager, player, animation_path)
        self.name = name
        self.level = level
        self.map_manager = map_manager
        self.player = player
        self.get_data()
        self.munitions = self.map_manager.player.munitions[self.munition_type]

    def fire_attack(self):
        if self.munitions > 0:
            self.munitions -= 1
            p = Projectil(self.map_manager)
            self.map_manager.get_map().projectils.append(p)
            self.map_manager.get_map().group.add(p)
