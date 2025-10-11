import pygame
from knight_path.Entity import Entity
from knight_path.const import WIN_HEIGHT

class Player(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.speed = 5
        self.jump_strength = 15
        self.gravity = 1
        self.vel_y = 0
        self.is_jumping = False
        self.is_attacking = False

        # ===== Animação =====
        self.walk_frames = [pygame.image.load(f'./assets/images/RogueWalk{n}.png') for n in range(1, 4)]
        self.attack_frames = [pygame.image.load(f'./assets/images/RogueAttack{n}.png') for n in range(1, 4)]
        self.jump_frames = [pygame.image.load(f'./assets/images/RogueJump{n}.png') for n in range(1, 3)]
        self.idle_frame = pygame.image.load('./assets/images/RogueIdle.png')

        self.current_frame = 0
        self.frame_counter = 0
        self.facing_right = True

        # Controle de ataque
        self.attack_frame_counter = 0
        self.attack_frame_speed = 10
        self.attack_duration = len(self.attack_frames) * self.attack_frame_speed
        self.attack_timer = 0  # conta o tempo de ataque

        # Controle de pulo
        self.jump_frame_counter = 0
        self.jump_frame_speed = 4

    def move(self, keys):
        moving = False

        # Movimento lateral
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.facing_right = True
            moving = True

        # Pular
        if not self.is_jumping and keys[pygame.K_SPACE]:
            self.is_jumping = True
            self.vel_y = -self.jump_strength

        # Gravidade
        if self.is_jumping:
            self.rect.y += self.vel_y
            self.vel_y += self.gravity
            if self.rect.bottom >= WIN_HEIGHT - 50:
                self.rect.bottom = WIN_HEIGHT - 50
                self.is_jumping = False

        # ===== Ataque =====
        self.attack(keys)

        # ===== Animação =====
        if self.is_attacking:
            self.attack_frame_counter += 1
            self.attack_timer -= 1
            if self.attack_frame_counter >= self.attack_frame_speed:
                self.attack_frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
            self.surf = self.attack_frames[self.current_frame]

            # Encerra o ataque quando o tempo acabar
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

        # Flip horizontal se estiver para a esquerda
        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)

    def attack(self, keys):
        # Inicia o ataque apenas quando a tecla Z é pressionada (1x)
        if keys[pygame.K_z] and not self.is_attacking:
            self.is_attacking = True
            self.current_frame = 0
            self.attack_frame_counter = 0
            self.attack_timer = self.attack_duration
            print("Ataque com espada!")
