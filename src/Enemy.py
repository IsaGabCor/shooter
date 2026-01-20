import pygame

vec = pygame.math.Vector2

RED = (200, 50, 50)

class Enemy:
    def __init__(self, pos, size=16):
        self.pos = vec(pos)
        self.size = size

        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = self.pos

        self.health = 3
        self.alive = True

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False

    def update(self):
        # No movement yet (intentional)
        self.rect.center = self.pos

    def draw(self, surface, cam):
        screen_pos = cam.world_to_screen(self.rect.topleft)

        draw_rect = pygame.Rect(
            screen_pos[0],
            screen_pos[1],
            self.rect.width,
            self.rect.height
        )

        # Body
        pygame.draw.rect(surface, RED, draw_rect)

        # Debug outline
        pygame.draw.rect(surface, (255, 255, 255), draw_rect, 1)

        # Health bar (debug)
        bar_width = self.size
        bar_height = 3
        health_ratio = max(self.health / 3, 0)

        bar_x = draw_rect.left
        bar_y = draw_rect.top - 6

        bg = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        fg = pygame.Rect(bar_x, bar_y, bar_width * health_ratio, bar_height)

        pygame.draw.rect(surface, (40, 40, 40), bg)
        pygame.draw.rect(surface, (0, 255, 0), fg)

