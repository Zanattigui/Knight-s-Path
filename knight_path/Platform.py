import pygame
from knight_path.Entity import Entity

class Platform(Entity):
    def __init__(self, name, position, size):
        # cria uma superfície simples (retângulo) pra representar a plataforma
        self.surf = pygame.Surface(size)
        self.surf.fill((139, 69, 19))  # cor marrom pra visualizar
        self.rect = self.surf.get_rect(topleft=position)

        # propriedades herdadas
        self.name = name
        self.speed = 0

    def move(self, *args):
        pass  # as plataformas não se movem por enquanto
