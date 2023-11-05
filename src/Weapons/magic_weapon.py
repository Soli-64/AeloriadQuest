from src.Weapons.weapon import Weapon


class MagicWeapon(Weapon):

    def __init__(self, name, level, map_manager):
        super().__init__(name, level, map_manager)
        self.name = name
        self.level = level
        self.map_manager = map_manager
        self.player = self.map_manager.player

    def magic_attack(self):
        for enemy in self.map_manager.get_map().enemys:
            knock_stats = self.player.localize(enemy, self.player.reach + self.reach)
            if knock_stats:
                enemy.apply_damage(self.damage)
