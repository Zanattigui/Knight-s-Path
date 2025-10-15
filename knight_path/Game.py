import pygame

from knight_path.Level import Level
from knight_path.Menu import Menu
from knight_path.const import MENU_OPTION, WIN_HEIGHT, WIN_WIDTH

class Game:
    def __init__(self):
        self.window = None
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


    def run(self):

        pygame.display.set_caption("Knight’s Path")
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()
            
            if menu_return in [MENU_OPTION[0]]:
                level = Level(self.window, 'level1')
                level_return = level.run()
            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                quit()
            else:
                pass
        