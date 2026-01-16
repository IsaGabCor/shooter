class Level:
    def __init__(self):
        self.bullets = []

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def update_level(self, window, cam):
        print(len(self.bullets))
        for b in self.bullets:
            if b.alive:
                b.update_bullet(window, cam)
            else:
                self.bullets.remove(b)
