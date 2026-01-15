import pygame

class Camera:
    def __init__(self, width, height):
        self.pos = pygame.math.Vector2(0, 0)
        self.width = width
        self.height = height

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
            (world_pos[0] - self.pos.x),
            (world_pos[1] - self.pos.y)
        )

    def screen_to_world(self, screen_pos):
        return (
            screen_pos[0] + self.pos.x,
            screen_pos[1] + self.pos.y
        )