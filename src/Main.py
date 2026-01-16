import pygame, sys, os, json
import Player, Level, Tiles, Camera, Sounds

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()


#SYSTEM/WINDOW CONSTANTS
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 256
map_scale = 3
FPS = 60

with open("./src/WeaponList.json") as f:
    WEAPON_DATA = json.load(f)

FramePerSec = pygame.time.Clock()
pygame.display.set_caption("WIP")
DisplayWindow = pygame.display.set_mode((SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
DISPLAY_W, DISPLAY_H = DisplayWindow.get_size()
world = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

#cursor handling
pygame.event.set_grab(True)  # confines cursor to window
pygame.mouse.set_visible(False)  # hides the OS cursor
pygame.mouse.set_pos(DISPLAY_W // 2, DISPLAY_H // 2)

#GAME CONSTANTS
running = True

#level/maps
tile_map = "./Assets/Maps/map2.csv"
level = Level.Level()
level_map = Tiles.TileMap(tile_map)
map_width = level_map.width * level_map.tile_size
map_height = level_map.height * level_map.tile_size

#sounds
sounds = Sounds.SoundManager()
sounds.load_sounds()

#camera
cam = Camera.Camera(VIRTUAL_WIDTH, VIRTUAL_HEIGHT)
center = (VIRTUAL_WIDTH//2, VIRTUAL_HEIGHT//2) # center right now is mostly for debug

#players
p1 = Player.Player((300,500), WEAPON_DATA[1])
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

    cam.update_shake()
    cam.follow(p1, map_width, map_height)

    world.fill((10, 10, 10))
    draw_world(world, cam)

    p1.player_update(world, cam, level, map_width, map_height, sounds) 
    level.update_level(world, cam)
    

    #dummy.player_update(DisplayWindow, p1.pos)

    #DEBUGLINE
    #pygame.draw.circle(world, (255,0,0), center, 3)

    pygame.transform.scale(world, DisplayWindow.get_size(), DisplayWindow)


    pygame.display.update()
    FramePerSec.tick(FPS)

