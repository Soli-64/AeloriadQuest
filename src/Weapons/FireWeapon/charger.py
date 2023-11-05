import src.Utils.pg_utils as f_pg


class Charger:

    def __init__(self, map_manager, munition_type):
        self.name = f'charger_{munition_type}'
        self.map_manager = map_manager
        self.munition_type = munition_type
        self.size = 20
        self.item_image = f_pg.pygame_image('./assets/images/weapons/charger/charger.png', [50, 50])

    def use(self):
        self.map_manager.player.munitions[self.munition_type] += self.size
        self.map_manager.player.inventory["chargers"].remove(self)
