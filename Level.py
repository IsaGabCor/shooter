class Level:
    def __init__(self):
        self.bullets = []

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def update_level(self, window):
        print(len(self.bullets))
        for b in self.bullets:
            if b.alive:
                b.update_bullet(window)
            else:
                self.bullets.remove(b)
