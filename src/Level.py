class Level:
    def __init__(self):
        #self.bullets = []
        pass

    #def add_bullet(self, bullet):
        #self.bullets.append(bullet)

    def update_level(self, window, cam, level, enemies):
        #print(len(self.bullets))
        # for b in self.bullets:
        #     if b.alive:
        #         b.update_bullet(window, cam, level, enemies)
        #     else:
        #         self.bullets.remove(b)
        pass

    def check_collision(self, rect, tilemap):
        for wall in tilemap.collision_rects:
            if rect.colliderect(wall):
                return wall
        return None

