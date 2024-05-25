class Obstacles:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def collide(self, x, y):
        if x < self.x + self.width and x + 40 > self.x:
            if y < self.y + self.height and y + 40 > self.y:
                return True
        return False