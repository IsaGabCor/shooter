import pygame
import Weapon


pygame.font.init()

#WORLD CONSTANTS
WHITE = (255, 255, 255)

#PLAYER CONSTANTS
vec = pygame.math.Vector2
FRIC = -0.12
ACC = 0.6
MAX_SPEED = 2

class Player:
    def __init__(self, pos, weapon_data):
        super().__init__()
        self.surf = pygame.Surface((10,14))
        self.surf.fill((125, 125, 125))
        self.rect = self.surf.get_rect()


        self.pos = vec(pos)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hitbox = (0, 0)
        self.state = "idle"
        self.weapon = Weapon.Weapon(weapon_data)
        self.health = 100

    def player_update(self, window, cam, level, map_width, map_height, sfx, level_map, bullet_mngr):
        pressed_keys = pygame.key.get_pressed()
        mouse_click = pygame.mouse.get_pressed()[0]
        #mouse_pos = pygame.mouse.get_pos()
        screen_pos = cam.screen_to_world(pygame.mouse.get_pos())

        self.input(pressed_keys)
        self.physics(level, level_map)
        self.player_draw(window, cam)
        self.weapon.update_weapon(self.pos, screen_pos, window, cam, )
        if mouse_click:
            self.use_weapon(level, screen_pos, cam, sfx, bullet_mngr)
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

    def physics(self, level, level_map):
        # Apply friction
        self.acc += self.vel * FRIC

        # Integrate velocity
        self.vel += self.acc

        # Clamp max speed
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        # --- X movement ---
        self.pos.x += self.vel.x
        self.rect.x = round(self.pos.x)

        hit = level.check_collision(self.rect, level_map)
        if hit:
            if self.vel.x > 0:
                self.rect.right = hit.left
            elif self.vel.x < 0:
                self.rect.left = hit.right
            self.pos.x = self.rect.x
            self.vel.x = 0

        # --- Y movement ---
        self.pos.y += self.vel.y
        self.rect.y = round(self.pos.y)

        hit = level.check_collision(self.rect, level_map)
        if hit:
            if self.vel.y > 0:
                self.rect.bottom = hit.top
            elif self.vel.y < 0:
                self.rect.top = hit.bottom
            self.pos.y = self.rect.y
            self.vel.y = 0


    def use_weapon(self, level, screen_pos, cam, sfx, bullet_mngr):
            self.weapon.fire(screen_pos, self, level, cam, sfx, bullet_mngr)

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

