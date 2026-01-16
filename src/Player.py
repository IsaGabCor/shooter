import pygame
import Weapon


pygame.font.init()

#WORLD CONSTANTS
WHITE = (255, 255, 255)

#PLAYER CONSTANTS
vec = pygame.math.Vector2
FRIC = -0.12
ACC = 0.3

class Player:
    def __init__(self, pos, weapon_data):
        super().__init__()
        self.surf = pygame.Surface((16,16))
        self.surf.fill((125, 125, 125))
        self.rect = self.surf.get_rect()


        self.pos = vec(pos)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hitbox = (0, 0)
        self.state = "idle"
        self.weapon = Weapon.Weapon(weapon_data)
        self.health = 100

    def player_update(self, window, cam, level, map_width, map_height, sfx):
        pressed_keys = pygame.key.get_pressed()
        mouse_click = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        screen_pos = cam.screen_to_world(mouse_pos)

        self.input(pressed_keys)
        self.physics(map_width, map_height)
        self.player_draw(window, cam)
        self.weapon.update_weapon(self.pos, screen_pos, window, cam)
        if mouse_click:
            self.use_weapon(level, screen_pos, cam, sfx)
        self.display_player_stats(window)
        
    def input(self, keys):
        self.acc = vec(0,0)
        if keys[pygame.K_w]:
            self.acc.y = -ACC
        if keys[pygame.K_s]:
            self.acc.y = ACC
        if keys[pygame.K_a]:
            self.acc.x = -ACC
        if keys[pygame.K_d]:
            self.acc.x = ACC
        if keys[pygame.K_r]:
            self.weapon.reload()
        if keys[pygame.K_ESCAPE]:
            pygame.event.set_grab(False)  
            pygame.mouse.set_visible(True)

    def physics(self, map_width, map_height):
        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #bounds check
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > map_width - 16:
            self.pos.x = map_width - 16
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > map_height - 16:
            self.pos.y = map_height - 16

        self.rect.center = self.pos

    def use_weapon(self, level, screen_pos, cam, sfx):
            self.weapon.fire(screen_pos, self, level, cam, sfx)

    def display_player_stats(self, window):
        # Font (use a default system font)
        font = pygame.font.Font(None, 26)
        gun_surface = font.render(self.weapon.name, True, WHITE)
        ammo_surface = font.render((str(self.weapon.current_ammo) + "/" + str(self.weapon.mag_size)), True, WHITE)

        window.blit(gun_surface, (0, 0))
        window.blit(ammo_surface, (0, 28))


    def player_draw(self, window, cam):
        screen_pos = cam.world_to_screen(self.rect.topleft)
        window.blit(self.surf, screen_pos)

        # DEBUG: draw rect
        #debug_rect = pygame.Rect(screen_pos, self.rect.size)
        #pygame.draw.rect(window, (0,255,0), debug_rect, 1)

        # DEBUG: draw player center
        #font = pygame.font.Font(None, 18)
        #text = font.render(str(self.rect.center), True, (255,255,0))
        #window.blit(text, (10,40))


