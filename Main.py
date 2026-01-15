import pygame
import sys
import json
import Player, Level, Tiles, Camera

pygame.init()

#SYSTEM/WINDOW CONSTANTS
#WIDTH = 960
#HEIGHT = 768
VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 256
map_scale = 3
FPS = 60

with open("WeaponList.json") as f:
    WEAPON_DATA = json.load(f)

FramePerSec = pygame.time.Clock()
pygame.display.set_caption("WIP")
DisplayWindow = pygame.display.set_mode((VIRTUAL_WIDTH * map_scale, VIRTUAL_HEIGHT * map_scale))
pygame.event.set_grab(True)  # confines cursor to window
pygame.mouse.set_visible(False)  # hides the OS cursor

world = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

#GAME CONSTANTS
running = True

#level/maps
tile_map = "./Assets/Maps/map1.csv"
level = Level.Level()
level_map = Tiles.TileMap(tile_map)
map_width = level_map.width * level_map.tile_size
map_height = level_map.height * level_map.tile_size

print(map_width, map_height)


#camera
cam = Camera.Camera(VIRTUAL_WIDTH, VIRTUAL_HEIGHT)
center = (VIRTUAL_WIDTH//2, VIRTUAL_HEIGHT//2)

#players
p1 = Player.Player((0,0), WEAPON_DATA[2])
#dummy = Player.Player((200,100))

#helper functions
def draw_world(world, cam):
    for tile in level_map.tiles:
        screen_pos = cam.world_to_screen(tile.rect.topleft)
        world.blit(tile.image, screen_pos)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    cam.follow(p1, map_width, map_height)

    world.fill((10, 10, 10))
    draw_world(world, cam)

    p1.player_update(world, cam, level, map_width, map_height) 
    level.update_level(world)

    #dummy.player_update(DisplayWindow, p1.pos)

    pygame.transform.scale(world, DisplayWindow.get_size(), DisplayWindow)
    pygame.display.update()
    FramePerSec.tick(FPS)

