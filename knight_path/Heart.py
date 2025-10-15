import pygame
from knight_path.Entity import Entity

class Heart(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)

        # Carrega a imagem do coração
        try:
            self.surf = pygame.image.load('./assets/images/Heart.png').convert_alpha()
            # Redimensiona se necessário, por exemplo, para 32x32 pixels
            self.surf = pygame.transform.scale(self.surf, (32, 32)) 
        except pygame.error:
            # Se a imagem não carregar, cria uma superfície vermelha para não quebrar o jogo
            self.surf = pygame.Surface((32, 32))
            self.surf.fill((255, 0, 0))

        # Define a posição e a caixa de colisão
        self.rect = self.surf.get_rect(center=position)

    def move(self):
        # O coração é um item estático, então o método move não faz nada
        pass