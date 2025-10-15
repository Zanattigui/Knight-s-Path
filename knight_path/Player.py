import pygame
from knight_path.Entity import Entity
from knight_path.const import WIN_HEIGHT, WIN_WIDTH

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
        self.max_health = 10
        self.is_hurt = False
        self.is_dead = False
        self.death_animation_finished = False
        self.hurt_timer = 0
        self.hurt_duration = 30

        # Animações
        self.idle_frame = pygame.image.load('./assets/images/KnightIdle.png')
        self.walk_frames = [pygame.image.load(f'./assets/images/KnightWalk{n}.png') for n in range(1, 6)]
        self.attack_frames = [pygame.image.load(f'./assets/images/KnightAttack{n}.png') for n in range(1, 6)]
        self.jump_frames = [pygame.image.load(f'./assets/images/KnightJump{n}.png') for n in range(1, 8)]
        self.hurt_frame = pygame.image.load('./assets/images/KnightHurt.png')
        self.death_frames = [pygame.image.load(f'./assets/images/KnightDead{n}.png') for n in range(1, 11)]

        # Índices de frame
        self.walk_frame_index = 0
        self.jump_frame_index = 0
        self.attack_frame_index = 0
        self.death_frame_index = 0

        # Contadores
        self.walk_frame_counter = 0
        self.death_frame_counter = 0
        self.jump_frame_counter = 0
        self.attack_frame_counter = 0
        self.attack_duration = len(self.attack_frames) * 10
        self.attack_timer = 0
        self.jump_frame_speed = 4
        self.attack_frame_speed = 10
        self.walk_frame_speed = 10
        self.death_frame_speed = 8

        self.facing_right = True

    def move(self, keys, platforms=[], enemies=[]):
        if self.is_dead:
            self.update_death_animation()
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

        # Limita o movimento do jogador dentro da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0

        self.vel_y += self.gravity
        if keys[pygame.K_w] and not self.is_jumping:
            self.vel_y = -self.jump_strength
            self.is_jumping = True

        self.rect.y += self.vel_y

        # Checa colisão com chão
        on_ground = False
        if self.rect.bottom >= WIN_HEIGHT - 50:
            self.rect.bottom = WIN_HEIGHT - 50
            self.vel_y = 0
            on_ground = True

        # Checa colisão com plataformas
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                if self.rect.bottom - self.vel_y <= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    on_ground = True

        self.is_jumping = not on_ground

        # Ataque
        self.attack(keys, enemies)

        # Atualiza animação
        old_midbottom = self.rect.midbottom

        # Atualiza a imagem (surf) de acordo com o estado
        if self.is_hurt:
            self.hurt_timer -= 1
            self.surf = self.hurt_frame
            if self.hurt_timer <= 0:
                self.is_hurt = False

        elif self.is_attacking:
            self.attack_frame_counter += 1
            if self.attack_frame_counter >= self.attack_frame_speed:
                self.attack_frame_counter = 0
                self.attack_frame_index = (self.attack_frame_index + 1) % len(self.attack_frames)
            self.surf = self.attack_frames[self.attack_frame_index]

            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False

        elif self.is_jumping:
            self.jump_frame_counter += 1
            if self.jump_frame_counter >= self.jump_frame_speed:
                self.jump_frame_counter = 0
                self.jump_frame_index = (self.jump_frame_index + 1) % len(self.jump_frames)
            self.surf = self.jump_frames[self.jump_frame_index]

        elif moving:
            self.walk_frame_counter += 1
            if self.walk_frame_counter >= self.walk_frame_speed:
                self.walk_frame_counter = 0
                self.walk_frame_index = (self.walk_frame_index + 1) % len(self.walk_frames)
            self.surf = self.walk_frames[self.walk_frame_index]

        else:
            self.surf = self.idle_frame

        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)
        
        self.rect = self.surf.get_rect(midbottom=old_midbottom)

    def take_damage(self, amount=1):
        if not self.is_hurt:
            self.health -= amount
            self.is_hurt = True
            self.hurt_timer = self.hurt_duration

            if self.health <= 0:
                self.is_dead = True
                self.death_frame_index = 0

    def update_death_animation(self):
        if self.death_frame_index < len(self.death_frames) - 1:
            self.death_frame_counter += 1
            if self.death_frame_counter >= self.death_frame_speed:
                self.death_frame_counter = 0
                self.death_frame_index += 1
            self.surf = self.death_frames[self.death_frame_index]
        else:
            self.surf = self.death_frames[-1]
            self.death_animation_finished = True

    def attack(self, keys, enemies):
        if pygame.mouse.get_pressed()[0] and not self.is_attacking:
            self.is_attacking = True
            self.attack_frame_index = 0
            self.attack_frame_counter = 0
            self.attack_timer = self.attack_duration

            attack_rect = self.rect.copy()
            if self.facing_right:
                attack_rect.x += self.rect.width
            else:
                attack_rect.x -= self.rect.width
            attack_rect.width = 50
            attack_rect.height = self.rect.height

            for enemy in enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.take_damage()

    def heal(self, amount=1):
        if self.health < self.max_health:
            self.health += amount
            # Garante que a vida não ultrapasse o máximo
            if self.health > self.max_health:
                self.health = self.max_health