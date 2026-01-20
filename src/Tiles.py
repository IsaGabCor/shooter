import pygame, pytmx

#sheet_png = "./Assets/map_sheets/level_sheet.png"
#map_scale = 3

class Tile(pygame.sprite.Sprite):
    def __init__ (self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = (x,y))

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))



class TileMap:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)

        self.tile_size = self.tmx_data.tilewidth
        self.width = self.tmx_data.width
        self.height = self.tmx_data.height

        self.pixel_width = self.width * self.tile_size
        self.pixel_height = self.height * self.tile_size

        self.tiles = []          # visual tiles
        self.collision_rects = []  # solid geometry

        self.load_tiles()
        self.load_collisions()
        self.load_spawns()

    def load_tiles(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        rect = tile.get_rect()
                        rect.topleft = (
                            x * self.tile_size,
                            y * self.tile_size
                        )
                        self.tiles.append((tile, rect))

    def load_collisions(self):
        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "Collisions":
                    for obj in layer:
                        rect = pygame.Rect(
                            obj.x,
                            obj.y,
                            obj.width,
                            obj.height
                        )
                        self.collision_rects.append(rect)

    def load_spawns(self):
        self.player_1_spawn = None
        self.enemy_spawns = []
        self.gun_spawns = []
        self.ammo_spawns = []

        for layer in self.tmx_data.layers:
            if not isinstance(layer, pytmx.TiledObjectGroup):
                continue

            if layer.name != "Entities":
                continue

            for obj in layer:
                pos = pygame.Vector2(obj.x, obj.y)

                if obj.type == "player_1_spawn":
                    self.player_1_spawn = pos

                elif obj.type == "enemy_spawn":
                    enemy_type = obj.properties.get("enemy_type", "grunt")
                    self.enemy_spawns.append({
                        "pos": pos,
                        "type": enemy_type
                    })

                elif obj.type == "gun_spawn":
                    weapon_name = obj.properties.get("weapon", "Pistol")
                    self.gun_spawns.append({
                        "pos": pos,
                        "weapon": weapon_name
                    })

                elif obj.type == "ammo_spawn":
                    amount = obj.properties.get("amount", 10)
                    self.ammo_spawns.append({
                        "pos": pos,
                        "amount": amount
                    })

        

    def draw_collisions(self, surface, camera):
        for rect in self.collision_rects:
            screen_pos = camera.world_to_screen(rect.topleft)
            debug_rect = pygame.Rect(
                screen_pos[0],
                screen_pos[1],
                rect.width,
                rect.height
            )
            pygame.draw.rect(surface, (255, 0, 0), debug_rect, 1)

    def draw_spawns_debug(self, surface, cam):
        if self.player_spawn:
            pygame.draw.circle(
                surface, (0, 255, 0),
                cam.world_to_screen(self.player_spawn),
                5
            )

        for e in self.enemy_spawns:
            pygame.draw.circle(
                surface, (255, 0, 0),
                cam.world_to_screen(e["pos"]),
                5
            )

        for g in self.gun_spawns:
            pygame.draw.circle(
                surface, (0, 0, 255),
                cam.world_to_screen(g["pos"]),
                4
            )

        for a in self.ammo_spawns:
            pygame.draw.circle(
                surface, (255, 255, 0),
                cam.world_to_screen(a["pos"]),
                4
            )




