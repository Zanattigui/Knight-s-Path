import pygame
from knight_path.Entity import Entity
from knight_path.EntityFactory import EntityFactory


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode

        self.entity_list: list[Entity] = []

        # Cria o fundo
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))

        # Cria o player
        self.player = EntityFactory.get_entity('Player', (100, 200))
        self.entity_list.append(self.player)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            # ===== Eventos =====
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            keys = pygame.key.get_pressed()

            # ===== Atualiza =====
            for ent in self.entity_list:
                if "keys" in ent.move.__code__.co_varnames:
                    ent.move(keys)
                else:
                    ent.move()

                self.window.blit(source=ent.surf, dest=ent.rect)

            pygame.display.flip()
            clock.tick(60)
