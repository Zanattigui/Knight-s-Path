import pygame
import random
from knight_path.Entity import Entity
from knight_path.EntityFactory import EntityFactory
from knight_path.Platform import Platform
from knight_path.Player import Player
from knight_path.const import WIN_WIDTH


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode

        self.entity_list: list[Entity] = []
        self.enemy_list: list[Entity] = []

        # Cria o fundo
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))

        # Cria o player
        self.player = EntityFactory.get_entity('Player', (100, 220))
        self.entity_list.append(self.player)

        # Cria as plataformas
        self.platforms = [
            Platform("Platform1", (25, 175), (150, 20)),
            Platform("Platform2", (400, 175), (150, 20)),
            Platform("Platform3", (190, 100), (180, 20))
        ]
        self.entity_list.extend(self.platforms)

        self.enemy_spawn_delay = 5000
        self.last_enemy_spawn_time = 0

    def run(self):
        clock = pygame.time.Clock()

        while True:
            # ===== Eventos =====
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            keys = pygame.key.get_pressed()

            current_time = pygame.time.get_ticks()

            if current_time - self.last_enemy_spawn_time > self.enemy_spawn_delay:
                self.last_enemy_spawn_time = current_time

                spawn_y = 0
                
                spawn_x = random.choice([25, 400, 100, 200, 300])
                if spawn_x == 25 or spawn_x == 400:
                    spawn_y = 125
                else:
                    spawn_y = 220

                new_enemy = EntityFactory.get_entity('Enemy1', (spawn_x, spawn_y))

                self.entity_list.append(new_enemy)
                self.enemy_list.append(new_enemy)

                print(f"Novo inimigo criado em ({spawn_x}, {spawn_y})! Total: {len(self.enemy_list)}")

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
