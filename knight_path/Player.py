import pygame
from knight_path.Entity import Entity
from knight_path.const import WIN_HEIGHT

class Player(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.speed = 3
        self.jump_strength = 15
        self.gravity = 1
        self.vel_y = 0
        self.is_jumping = False
        self.is_attacking = False
        self.health = 10
        self.is_hurt = False
        self.is_dead = False
        self.hurt_timer = 0
        self.hurt_duration = 30

        self.hurt_frame = pygame.image.load('./assets/images/RogueHurt.png')

        # Animação
        self.walk_frames = [pygame.image.load(f'./assets/images/RogueWalk{n}.png') for n in range(1, 4)]
        self.attack_frames = [pygame.image.load(f'./assets/images/RogueAttack{n}.png') for n in range(1, 4)]
        self.jump_frames = [pygame.image.load(f'./assets/images/RogueJump{n}.png') for n in range(1, 4)]
        self.idle_frame = pygame.image.load('./assets/images/RogueIdle.png')
        self.death_frames = [pygame.image.load(f'./assets/images/RogueDead{n}.png') for n in range(1, 11)]

        self.current_frame = 0
        self.frame_counter = 0
        self.facing_right = True

        # Controle de ataque
        self.attack_frame_counter = 0
        self.attack_frame_speed = 10
        self.attack_duration = len(self.attack_frames) * self.attack_frame_speed
        self.attack_timer = 0

        # Controle de pulo
        self.jump_frame_counter = 0
        self.jump_frame_speed = 4

        self.death_frame_counter = 0
        self.death_frame_speed = 8
        self.death_finished = False

    def move(self, keys, platforms=[], enemies=[]):
        if self.is_dead:
            if not self.death_finished:
                self.death_frame_counter += 1
                if self.death_frame_counter >= self.death_frame_speed:
                    self.death_frame_counter = 0
                    self.current_frame += 1
                    if self.current_frame >= len(self.death_frames):
                        self.current_frame = len(self.death_frames) - 1
                        self.death_finished = True
                self.surf = self.death_frames[self.current_frame]

                if not self.facing_right:
                    self.surf = pygame.transform.flip(self.surf, True, False)
            return

        moving = False
        # Movimento lateral
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing_right = False
            moving = True
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing_right = True
            moving = True

        self.vel_y += self.gravity
        
        if keys[pygame.K_w] and not self.is_jumping:
            self.vel_y = -self.jump_strength
            self.is_jumping = True

        self.rect.y += self.vel_y

        on_ground = False

        if self.rect.bottom >= WIN_HEIGHT - 50:
            self.rect.bottom = WIN_HEIGHT - 50
            self.vel_y = 0
            on_ground = True

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                if self.rect.bottom - self.vel_y <= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    on_ground = True
        
        if on_ground:
            self.is_jumping = False
        else:
            self.is_jumping = True

        # Ataque
        self.attack(keys, enemies)

        # Animação
        if self.is_attacking:
            self.attack_frame_counter += 1
            self.attack_timer -= 1
            if self.attack_frame_counter >= self.attack_frame_speed:
                self.attack_frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
            self.surf = self.attack_frames[self.current_frame]

            if self.attack_timer <= 0:
                self.is_attacking = False

        elif self.is_jumping:
            self.jump_frame_counter += 1
            if self.jump_frame_counter >= self.jump_frame_speed:
                self.jump_frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
            self.surf = self.jump_frames[self.current_frame]

        elif moving:
            self.frame_counter += 1
            if self.frame_counter >= 10:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            self.surf = self.walk_frames[self.current_frame]

        else:
            self.surf = self.idle_frame

        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)

        # Animação
        if self.is_attacking:
            self.attack_frame_counter += 1
            self.attack_timer -= 1
            if self.attack_frame_counter >= self.attack_frame_speed:
                self.attack_frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
            self.surf = self.attack_frames[self.current_frame]

            if self.attack_timer <= 0:
                self.is_attacking = False

        elif self.is_jumping:
            self.jump_frame_counter += 1
            if self.jump_frame_counter >= self.jump_frame_speed:
                self.jump_frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
            self.surf = self.jump_frames[self.current_frame]

        elif moving:
            self.frame_counter += 1
            if self.frame_counter >= 10:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            self.surf = self.walk_frames[self.current_frame]

        else:
            self.surf = self.idle_frame

        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)

        # ===== Animação de dano =====
        if self.is_hurt:
            self.hurt_timer -= 1
            self.surf = self.hurt_frame
            if self.hurt_timer <= 0:
                self.is_hurt = False

    def take_damage(self, amount=1):
        if not self.is_hurt:
            self.health -= amount
            self.is_hurt = True
            self.hurt_timer = self.hurt_duration
            print(f"Player levou {amount} de dano! Vida restante: {self.health}")

            if self.health <= 0:
                self.is_dead = True
                self.current_frame = 0
                self.death_frame_counter = 0
                print("💀 Player morreu!")

    def update_death_animation(self):
        # Toca a animação de morte quadro a quadro
        if self.death_frame_speed < len(self.death_frames) - 1:
            self.death_frame_counter += 1
            if self.death_frame_counter >= self.death_frame_speed:
                self.death_frame_counter = 0
                self.death_frame_speed += 1
            self.surf = self.death_frames[self.death_frame_speed]
        else:
            # Último frame (fica no chão morto)
            self.surf = self.death_frames[-5]

    def attack(self, keys, enemies):
        if pygame.mouse.get_pressed()[0] and not self.is_attacking:
            self.is_attacking = True
            self.current_frame = 0
            self.attack_frame_counter = 0
            self.attack_timer = self.attack_duration

            # Define a hitbox do ataque
            attack_rect = self.rect.copy()
            if self.facing_right:
                attack_rect.x += self.rect.width
            else:
                attack_rect.x -= self.rect.width
            attack_rect.width = 50  # largura do ataque
            attack_rect.height = self.rect.height

            # Verifica colisão com inimigos
            for enemy in enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.take_damage()
