import pygame

from knight_path.Menu import Menu
from knight_path.const import WIN_HEIGHT, WIN_WIDTH

class Game:
    def __init__(self):
        self.window = None
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


    def run(self):

        pygame.display.set_caption("Knight’s Path")
        while True:
            menu = Menu(self.window)
            menu.run()
            pass
        