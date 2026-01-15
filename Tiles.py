import pygame
import csv

sheet_png = "./Assets/map_sheets/level_sheet.png"
map_scale = 3

class SpriteSheet:
    def __init__(self, filename, tile_size):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.tile_size = tile_size
        self.columns = self.sheet.get_width() // tile_size

    def get_tile(self, tile_id):
        x = (tile_id % self.columns) * self.tile_size
        y = (tile_id // self.columns) * self.tile_size

        image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, self.tile_size, self.tile_size))
        return image


class Tile(pygame.sprite.Sprite):
    def __init__ (self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = (x,y))

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap:
    def __init__(self, filename):
        self.tile_size = 16
        self.width = 0
        self.height = 0
        self.tiles = []

        self.spritesheet = SpriteSheet(sheet_png, self.tile_size)
        self.load_tiles(filename)

    def read_csv(self, filename):
        data = []
        with open(filename) as file:
            reader = csv.reader(file)
            for row in reader:
                data.append([int(cell) for cell in row])
        return data

    def load_tiles(self, filename):
        tile_data = self.read_csv(filename)

        self.width = len(tile_data[0])
        self.height = len(tile_data)

        for y, row in enumerate(tile_data):
            for x, tile_id in enumerate(row):
                if tile_id == -1:
                    continue

                image = self.spritesheet.get_tile(tile_id)
                #image = pygame.transform.scale(image, (self.tile_size * map_scale, self.tile_size * map_scale))
                world_x = x * self.tile_size
                world_y = y * self.tile_size

                self.tiles.append(Tile(image, world_x, world_y))
