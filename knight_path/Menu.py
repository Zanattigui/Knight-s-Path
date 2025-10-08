import pygame

from knight_path.const import COLOR_ALE, COLOR_GRAY, COLOR_WHITE, MENU_OPTION, WIN_WIDTH
from pygame import Surface, Rect
from pygame.font import Font



class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./assets/images/menuBg.png')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self,):
        menu_option = 0
        pygame.mixer_music.load('./assets/sounds/menuSound.wav')
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "* Knight's Path *", COLOR_GRAY, ((WIN_WIDTH/2), 70))
            
            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(25, MENU_OPTION[i], COLOR_ALE, ((WIN_WIDTH / 2), 150 + (40 * i)))
                else:
                    self.menu_text(20, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2), 150 + (40 * i)))

            #Check
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

            pygame.display.flip()

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.Font("./assets/fonts/menuFont.ttf", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
        