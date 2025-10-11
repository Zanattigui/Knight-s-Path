import pygame
from knight_path.Entity import Entity
from knight_path.EntityFactory import EntityFactory
from knight_path.Platform import Platform
from knight_path.Player import Player


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

        # Cria as plataformas
        self.platforms = [
            Platform("Platform1", (25, 175), (150, 20)),
            Platform("Platform2", (400, 175), (150, 20)),
            Platform("Platform3", (190, 100), (180, 20))
        ]
        self.entity_list.extend(self.platforms)

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
                if isinstance(ent, Player):
                    ent.move(keys, self.platforms)
                elif "keys" in ent.move.__code__.co_varnames:
                    ent.move(keys)
                else:
                    ent.move()

                self.window.blit(source=ent.surf, dest=ent.rect)

            pygame.display.flip()
            clock.tick(60)
