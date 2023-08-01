from dataclasses import dataclass
from src.Enemy.enemy import Enemy
from src.Missioner.missioner import Missioner
import pygame, pyscroll, pytmx


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
    #npcs: list[NPC]
    #weapons: list[Weapon]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.current_map = "carte"
        self.screen = screen
        self.player = player
        self.register_map("carte", teleporters=[
            #Teleporter(from_world="carte", origin_point="start_mission", target_world="dungeon1", teleport_point="player")
        ], npcs=[], enemys=[
            #Enemy(self.player, self)
        ], missioners=[
            Missioner('missioners/robin', [300, 300], self)
        ])
        self.teleport_player("player")

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

            """if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0

                else:
                    sprite.speed = 2"""

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

        for sprite in self.get_map().enemys:

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def register_map(self, name, teleporters=[], npcs=[], enemys=[], missioners=[]):
        # --------------- charger la carte (tmx) -----------
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
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group.add(self.player)

        # récup les npc pour les ajouter au groupe
        for missioner in missioners:
            group.add(missioner)

        for enemy in enemys:
            group.add(enemy)

        # créer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, teleporters, enemys, missioners)

    def check_missioner_collision(self):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is Missioner:
                sprite.launch_mission()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collision()
        self.player.update_health_bar(self.screen)
        for enemy in self.get_map().enemys:
            enemy.save_location()
            enemy.move()
