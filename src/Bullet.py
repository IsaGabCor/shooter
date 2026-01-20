import pygame
import math

vec = pygame.math.Vector2

WHITE = (255, 255, 255)

class BulletManager:
    def __init__(self):
        self.bullets = []

    def spawn(self, bullet):
        self.bullets.append(bullet)

    def update(self, window, cam, level, enemies):
        for bullet in self.bullets[:]:
            bullet.update_bullet(window, cam, level, enemies)
            if not bullet.alive:
                self.bullets.remove(bullet)


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

    def update_bullet(self, window, cam, level, enemies):
        if not self.alive:
            return
        
        self.update_pos()
        self.check_collision(level, enemies)

        self.draw_bullet(window, cam)
        self.current_life -= 1
        if self.current_life <= 0:
            self.alive = False
            
    def check_collision(self, level, enemies):
        for rect in level.collision_rects:
            if self.hitbox.colliderect(rect):
                self.alive = False
                return
        
        for enemy in enemies:
            if enemy is self.owner:
                continue

            if self.hitbox.colliderect(enemy.rect):
                #damage needs to be adjusted per bullet (MAYBE LATER)
                enemy.take_damage(1)
                self.alive = False
                return
    
    def update_pos(self):
        vx = math.cos(self.angle) * self.speed
        vy = -math.sin(self.angle) * self.speed

        self.pos.x += vx
        self.pos.y += vy

        self.hitbox.center = self.pos
    
    def draw_bullet(self, window, cam):
        screen_pos = cam.world_to_screen(self.pos)
        pygame.draw.circle(window, WHITE, screen_pos, 2)

        #debug line
        #pygame.draw.rect(window, (255, 0, 0), pygame.Rect(cam.world_to_screen(self.hitbox.topleft), self.hitbox.size), 1)
