import pygame
import random
from knight_path.Entity import Entity
from knight_path.EntityFactory import EntityFactory
from knight_path.Platform import Platform
from knight_path.Player import Player
from knight_path.const import WIN_WIDTH
from knight_path.Enemy import Enemy


class Level:
    def __init__(self, window, name):
        self.window = window
        self.name = name

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

        self.is_game_over = False
        self.font = pygame.font.Font(None, 100)
        self.dead_text = self.font.render("DEAD", True, (200, 0, 0))
        self.dead_rect = self.dead_text.get_rect(center=(WIN_WIDTH // 2, 150))
        self.dead_alpha = 0
        self.dead_fade_speed = 5

        # ===== Botão de retorno =====
        self.button_font = pygame.font.Font(None, 50)
        self.button_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(center=(WIN_WIDTH // 2, 300))

        self.button_bg_color = (80, 80, 80)
        self.button_hover_color = (120, 120, 120)

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

            # ===== Checa se o player morreu =====
            if self.player.health <= 0:
                self.is_game_over = True

            # ===== Lógica se o jogo acabou =====
            if self.is_game_over:
                # mostra animação de morte
                self.player.update_death_animation()

                # limpa tela e desenha a animação + texto
                self.window.fill((0, 0, 0))
                if self.dead_alpha < 255:
                    self.dead_alpha += self.dead_fade_speed
                    if self.dead_alpha > 255:
                        self.dead_alpha = 255

                dead_text_surface = self.dead_text.copy()
                dead_text_surface.set_alpha(self.dead_alpha)
                self.window.blit(dead_text_surface, self.dead_rect)

                # ======== Botão de retorno ao menu ========
                font_button = pygame.font.Font(None, 50)
                button_text = font_button.render("Menu", True, (255, 255, 255))

                button_width, button_height = 100, 45
                button_x = self.window.get_width() // 2 - button_width // 2
                button_y = self.window.get_height() // 2 + 60

                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()[0]
                color_idle = (80, 80, 80)
                color_hover = (120, 120, 120)

                pygame.draw.rect(
                    self.window,
                    color_hover if button_rect.collidepoint(mouse_pos) else color_idle,
                    button_rect,
                    border_radius=15
                )

                text_rect = button_text.get_rect(center=button_rect.center)
                self.window.blit(button_text, text_rect)

                if button_rect.collidepoint(mouse_pos) and mouse_pressed:
                    return "menu"

                pygame.display.flip()

                clock.tick(10)
                continue

            if current_time - self.last_enemy_spawn_time > self.enemy_spawn_delay:
                self.last_enemy_spawn_time = current_time

                spawn_y = 0
                spawn_x = random.choice([25, 400, 100, 200, 300])
                spawn_y_goblin = 130 if spawn_x in [25, 400] else 230
                spawn_y_boss = 110 if spawn_x in [25, 400] else 210

                # Decide aleatoriamente entre goblin e boss ou baseado em pontuação
                if random.random() < 0.19:  # 10% chance de spawnar o boss
                    new_enemy = EntityFactory.get_entity('EnemyBoss', (spawn_x, spawn_y_boss))
                    print('Valkiria criada')
                else:
                    new_enemy = EntityFactory.get_entity('Enemy1', (spawn_x, spawn_y_goblin))

                new_enemy.target_player = self.player
                self.entity_list.append(new_enemy)
                self.enemy_list.append(new_enemy)

                print(f"Novo inimigo criado em ({spawn_x}, {spawn_y})! Total: {len(self.enemy_list)}")

            # ===== Atualiza =====
            for ent in self.entity_list[:]:  # copia da lista para remover sem erro
                if isinstance(ent, Player):
                    ent.move(keys, self.platforms)
                    ent.attack(keys, self.enemy_list)
                elif "keys" in ent.move.__code__.co_varnames:
                    ent.move(keys)
                else:
                    ent.move()

                # Remove inimigos mortos que já sumiram
                if isinstance(ent, Enemy):
                    if ent.is_dead and ent.alpha <= 0:
                        self.entity_list.remove(ent)
                        if ent in self.enemy_list:
                            self.enemy_list.remove(ent)
                        continue  # não precisa desenhar mais

                self.window.blit(source=ent.surf, dest=ent.rect)

            #borda nos personagens para debug
            # pygame.draw.rect(self.window, (255, 0, 0), self.player.rect, 2)

            # for enemy in self.enemy_list:
            #     pygame.draw.rect(self.window, (0, 0, 255), enemy.rect, 2)

            pygame.display.flip()
            clock.tick(60)
