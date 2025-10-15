import pygame
from knight_path.Entity import Entity

class EnemyBoss(Entity):
    def __init__(self, name_base, position, frames_count=24, patrol_range=(0, 0), speed=1):
        super().__init__(name_base + '1', position)

        # Carrega frames do chefe
        self.name_base = name_base
        self.type = "boss"
        self.frames = [pygame.image.load(f'./assets/images/{name_base}{i}.png')for i in range(frames_count)]
        self.attack_frames = [pygame.image.load(f'./assets/images/BossAttack{i}.png')for i in range(1, 7)]
        self.hurt_frames = [pygame.image.load(f'./assets/images/BossHurt{i}.png')for i in range(1, 13)]
        self.death_frames = [pygame.image.load(f'./assets/images/BossDead{i}.png') for i in range(1, 16)]

        self.is_attacking = False
        self.attack_frame_counter = 0
        self.attack_frame_speed = 6  # pode ser mais rápido ou mais lento que o goblin
        self.attack_range = 50  # alcance maior que goblin
        self.attack_time = 2000  # tempo entre ataques maior
        self.last_attack_time = 0

        self.current_frame = 0
        self.frame_counter = 0
        self.frame_speed = 8
        self.speed = speed
        self.alpha = 255

        # Patrulha
        self.start_x = position[0]
        self.patrol_range = patrol_range
        self.direction = 1

        # Vida do boss
        self.health = 10  # muito maior que goblin
        self.is_hurt = False
        self.hurt_timer = 0
        self.hurt_duration = len(self.hurt_frames) * 3
        self.is_dead = False
        self.death_frame_counter = 0
        self.death_frame_speed = 8
        self.death_finished = False

    def move(self):
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
            else:
                self.alpha -= 5
                if self.alpha < 0:
                    self.alpha = 0
                self.surf.set_alpha(self.alpha)
            return

        if self.is_hurt:
            self.hurt_timer += 1
            frame_index = (self.hurt_timer // 3) % len(self.hurt_frames)
            self.surf = self.hurt_frames[frame_index]

            if self.hurt_timer >= self.hurt_duration:
                self.is_hurt = False
                self.hurt_timer = 0
            return

        # Movimento de patrulha
        self.rect.x += self.speed * self.direction
        if self.rect.x < self.start_x + self.patrol_range[0] or self.rect.x > self.start_x + self.patrol_range[1]:
            self.direction *= -1

        # Checa ataque
        if hasattr(self, 'target_player') and self.rect.colliderect(self.target_player.rect):
            current_time = pygame.time.get_ticks()
            if not self.is_attacking and current_time - self.last_attack_time >= self.attack_time:
                self.is_attacking = True
                self.current_attack_frame = 0
                self.attack_frame_counter = 0
        else:
            self.is_attacking = False

        # Animação
        if self.is_attacking:
            self.attack_frame_counter += 1
            if self.attack_frame_counter >= self.attack_frame_speed:
                self.attack_frame_counter = 0
                self.current_attack_frame = (self.current_attack_frame + 1) % len(self.attack_frames)
            self.surf = self.attack_frames[self.current_attack_frame]

            if self.current_attack_frame == len(self.attack_frames) // 2:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time >= self.attack_time:
                    self.target_player.take_damage(2)  # boss causa mais dano
                    self.last_attack_time = current_time
        else:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_speed:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.surf = self.frames[self.current_frame]

        if self.direction < 0:
            self.surf = pygame.transform.flip(self.surf, True, False)

    def take_damage(self, amount=1):
        if not self.is_hurt:
            self.health -= amount
            self.is_hurt = True
            if self.health <= 0:
                self.is_dead = True
                self.current_frame = 0
                self.death_frame_counter = 0