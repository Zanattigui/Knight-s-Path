import pygame

from knight_path.Menu import Menu

class Game:
    def __init__(self):
        self.window = None
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))


    def run(self):

        pygame.display.set_caption("Knight’s Path")

        while True:
            menu = Menu(self.window)
            menu.run()
            pass


            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         quit()

        