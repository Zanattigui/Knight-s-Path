from knight_path.Entity import Entity
from knight_path.const import WIN_WIDTH

class Background(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)

    def move(self, ):
        self.rect.centerx -= 1
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH
        pass