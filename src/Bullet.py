import pygame
import math

vec = pygame.math.Vector2

WHITE = (255, 255, 255)

class Bullet:
    def __init__(self, strt_pos, speed, radius, lifetime, angle, owner):
        self.pos = vec(strt_pos)
        self.speed = speed
        self.lifetime = lifetime
        self.radius = radius
        self.owner = owner
        self.angle = angle
        
        self.hitbox = pygame.Rect(0, 0, radius * 2, radius * 2)
        self.hitbox.center = self.pos

        self.current_life = self.lifetime
        self.alive = True

    def update_bullet(self, window, cam):
        if self.current_life > 0:
            self.update_pos()
            self.draw_bullet(window, cam)
            self.current_life -= 1
        else:
            self.alive = False
            
    def check_collision(self):
        pass
    
    def update_pos(self):
        vx = math.cos(self.angle) * self.speed
        vy = -math.sin(self.angle) * self.speed

        self.pos[0] += vx
        self.pos[1] += vy
    
    def draw_bullet(self, window, cam):
        screen_pos = cam.world_to_screen(self.pos)
        pygame.draw.circle(window, WHITE, screen_pos, 2)
