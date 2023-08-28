from dataclasses import dataclass
from src.Enemy.enemy import Enemy
from src.Missioner.missioner import Missioner
import pygame, pyscroll, pytmx
from src.Items.item import Item
from src.Items.chest import Chest
from src.Missioner.mission import Mission
from src.Weapons.projectil import Projectil
from src.Traders.trader import Trader

@dataclass
class Teleporter:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    teleporters: list[Teleporter]
    enemys: list[Enemy]
    missioners: list[Missioner]
    items: list[Item, Chest]
    projectils: list[Projectil]
    traders: list[Trader]
    #npcs: list[NPC]
    #weapons: list[Weapon]

class MapManager:

    def __init__(self, screen, player, game):
        self.game = game
        self.maps = dict()
        self.current_map = "world"
        self.screen = screen
        self.player = player
        self.current_mission = None
        self.register_map("world", teleporters=[], enemys=[], missioners=[
            Missioner('Robin', self)
        ], items=[
            Chest(100, 100, self)
        ], projectils=[], traders=[
            Trader('Paul', [350, 300], self)
        ])
        self.teleport_player("player")

    # FONCTION LIES A LA CREATION D'ELEMENTS SUR LA MAP
    def get_teleporter(self, from_world, origin_point, target_world, teleport_point): return Teleporter(from_world, origin_point, target_world, teleport_point)

    def get_chest(self, x, y): return Chest(x, y, self)

    def get_missioner(self): return Missioner('Robin', self)


    # FONCTIONS LIES AUX COMPORTEMENT D'ELEMENTS SUR LA MAP

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()


    # FONCTIONS LIES AUX COLLISIONS

    def check_missioner_collision(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is Missioner:
                if type(self.current_mission) is Mission and self.current_mission.isFinished:
                    sprite.choose_texts('reward')
                    dialog_box.execute(sprite.end_mission, sprite)
                else:
                    sprite.choose_texts('mission')
                    mission = dialog_box.execute(sprite.launch_mission, sprite)
                    if type(mission) is Mission:
                        self.current_mission = mission

    def check_trader_collision(self, game):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is Trader:
                game.pause(False, True)

    def check_collision(self):

        for portal in self.get_map().teleporters:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        # collisions
        for sprite in self.get_group().sprites():

            if sprite.feet.collidelist(self.get_walls()) > -1:
                if type(sprite) is Projectil:
                    self.get_map().projectils.remove(sprite)
                    self.get_map().group.remove(sprite)
                else:
                    sprite.move_back()
            if sprite.feet.collidelist(self.get_map().items) > -1:
                if type(sprite) is Projectil:
                    self.get_map().projectils.remove(sprite)
                    self.get_map().group.remove(sprite)
                else:
                    sprite.move_back()

        for sprite in self.get_map().enemys:

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def check_chest_collision(self):
        for sprite in self.get_group().sprites():
            if type(sprite) is Chest and sprite.rect.colliderect(self.player.rect):
                sprite.obtain()

    def check_projectile_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)


    # FONCTION MOTEUR DU JEU

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def register_map(self, name, teleporters=[], enemys=[], missioners=[], items=[], projectils=[], traders=[]):
        # --------------- charger la carte (tmx) -----------
        print(name)
        tmx_data = pytmx.util_pygame.load_pygame(f"./map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # définir la liste de rectangle de collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.properties.get("collision"):
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # --------------- dessiner le groupe de cartes ------
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=9)

        group.add(self.player)

        for missioner in missioners:
            group.add(missioner)

        for enemy in enemys:
            group.add(enemy)

        for item in items:
            group.add(item)

        for projectil in projectils:
            group.add(projectil)

        for trader in traders:
            group.add(trader)

        # créer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, teleporters, enemys, missioners, items, projectils, traders)

    def update(self):
        self.get_group().update()
        self.check_collision()
        self.player.update_stats(self.screen)
        for enemy in self.get_map().enemys:
            enemy.save_location()
            enemy.move()
        for p in self.get_map().projectils:
            p.move()
            p.update()
