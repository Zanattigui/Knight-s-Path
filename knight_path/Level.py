import pygame
import random
from knight_path.EnemyBoss import EnemyBoss
from knight_path.Entity import Entity
from knight_path.EntityFactory import EntityFactory
from knight_path.Platform import Platform
from knight_path.Player import Player
from knight_path.const import WIN_WIDTH
from knight_path.Enemy import Enemy
from knight_path.Heart import Heart 


class Level:
    def __init__(self, window, name):
        self.window = window
        self.name = name

        self.entity_list: list[Entity] = []
        self.enemy_list: list[Entity] = []
        self.heart_list: list[Heart] = []

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

        self.heart_spawn_delay = 15000
        self.last_heart_spawn_time = 0
        self.max_hearts_on_screen = 3
        self.heal_sound = pygame.mixer.Sound("./assets/sounds/Heart.wav")

        self.is_game_over = False
        self.font = pygame.font.Font("./assets/fonts/menuFont.ttf", 100)
        self.dead_text = self.font.render("DEAD", True, (200, 0, 0))
        self.dead_rect = self.dead_text.get_rect(center=(WIN_WIDTH // 2, 150))
        self.dead_alpha = 0
        self.dead_fade_speed = 5

        # ===== Botão de retorno =====
        self.button_font = pygame.font.Font("./assets/fonts/menuFont.ttf", 50)
        self.button_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(center=(WIN_WIDTH // 2, 300))

        self.button_bg_color = (80, 80, 80)
        self.button_hover_color = (120, 120, 120)

        self.score = 0

    def draw_score(self):
        font = pygame.font.Font("./assets/fonts/menuFont.ttf", 40)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(text, (20, 20))

    def draw_health(self):
        font = pygame.font.Font("./assets/fonts/menuFont.ttf", 40)
        text = font.render(f"Vida: {self.player.health}", True, (200, 50, 50))
        self.window.blit(text, (420, 20))

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
            if self.player.death_animation_finished and not self.is_game_over:
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

                score_font = pygame.font.Font("./assets/fonts/menuFont.ttf", 35)
                score_text = score_font.render(f"Score: {self.score}", True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(WIN_WIDTH // 2, 80))
                self.window.blit(score_text, score_rect)

                # ======== Botão de retorno ao menu ========
                font_button = pygame.font.Font("./assets/fonts/menuFont.ttf", 50)
                button_text = font_button.render("Retornar ao menu", True, (255, 255, 255))

                button_width, button_height = 360, 50
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

                spawn_x = random.choice([25, 400, 100, 200, 300])
                spawn_y_goblin = 130 if spawn_x in [25, 400] else 230
                spawn_y_boss = 110 if spawn_x in [25, 400] else 210

                if random.random() < 0.19:
                    new_enemy = EntityFactory.get_entity('EnemyBoss', (spawn_x, spawn_y_boss))
                else:
                    new_enemy = EntityFactory.get_entity('Enemy1', (spawn_x, spawn_y_goblin))

                new_enemy.target_player = self.player
                self.entity_list.append(new_enemy)
                self.enemy_list.append(new_enemy)

                if (current_time - self.last_heart_spawn_time > self.heart_spawn_delay) and (len(self.heart_list) < self.max_hearts_on_screen):
                    self.last_heart_spawn_time = current_time

                    # Posições para o coração aparecer
                    spawn_positions = [(100, 145), (475, 145), (280, 70)]
                    spawn_pos = random.choice(spawn_positions)

                    new_heart = Heart("Heart", spawn_pos)
                    self.entity_list.append(new_heart)
                    self.heart_list.append(new_heart)

            for ent in self.entity_list[:]:
                if isinstance(ent, Player):
                    ent.move(keys, self.platforms)
                    ent.attack(keys, self.enemy_list)
                elif "keys" in ent.move.__code__.co_varnames:
                    ent.move(keys)
                else:
                    ent.move()

                # Remove inimigos mortos que já sumiram e soma pontuação
                if isinstance(ent, (Enemy, EnemyBoss)):
                    if ent.is_dead and ent.alpha <= 0:
                        if isinstance(ent, EnemyBoss):
                            self.score += 25
                        else:
                            self.score += 10

                        self.entity_list.remove(ent)
                        if ent in self.enemy_list:
                            self.enemy_list.remove(ent)

                        continue

                self.window.blit(source=ent.surf, dest=ent.rect)

            #borda nos personagens para debugar
            # pygame.draw.rect(self.window, (255, 0, 0), self.player.rect, 2)

            # for enemy in self.enemy_list:
            #     pygame.draw.rect(self.window, (0, 0, 255), enemy.rect, 2)

                    # ===== Lógica de Colisão com Corações =====
            for heart in self.heart_list[:]:
                if self.player.rect.colliderect(heart.rect):
                    self.player.heal(1)
                    self.heal_sound.play()
                    self.heart_list.remove(heart)
                    self.entity_list.remove(heart)

            self.draw_score()
            self.draw_health()

            pygame.display.flip()
            clock.tick(60)
