import pygame, random, math

class Camera:
    def __init__(self, width, height):
        self.pos = pygame.math.Vector2(0, 0)
        self.width = width
        self.height = height

        self.shake_strength = 0
        self.shake_decay = .5
        self.shake_offset = pygame.math.Vector2(0, 0)

    def follow(self, target, map_width, map_height):
        desired = pygame.math.Vector2(
            target.rect.centerx - self.width // 2,
            target.rect.centery - self.height // 2
        )

        #decimal is for smoothing strength
        self.pos += (desired - self.pos) * 0.3 

        #clamp camera to world
        self.pos.x = max(0, min(self.pos.x, map_width - self.width))
        self.pos.y = max(0, min(self.pos.y, map_height - self.height))
    
    def world_to_screen(self, world_pos):
        return (
            (world_pos[0] - self.pos.x + self.shake_offset[0]),
            (world_pos[1] - self.pos.y + self.shake_offset[1])
        )

    def screen_to_world(self, screen_pos):
        return (
            screen_pos[0] + self.pos.x,
            screen_pos[1] + self.pos.y
        )
    
    def add_shake(self, strength):
        self.shake_strength = max(self.shake_strength, strength)

    def update_shake(self):
        if self.shake_strength > 0.1:
            self.shake_offset.x = random.uniform(-self.shake_strength, self.shake_strength)
            self.shake_offset.y = random.uniform(-self.shake_strength, self.shake_strength)
            self.shake_strength *= self.shake_decay
        else:
            self.shake_offset.update(0, 0)

      
        