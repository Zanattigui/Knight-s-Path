import pygame
from knight_path.Entity import Entity

class Enemy(Entity):
    def __init__(self, name_base, position, frames_count=1, patrol_range=(0, 0), speed=0.5):
        super().__init__(name_base + '0', position)

        sprite_width = 50
        sprite_height = 50
        sprite_size = (sprite_width, sprite_height)

        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f'./assets/images/{name_base}{i}.png'),
                sprite_size
            ) for i in range(frames_count)
        ]
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_speed = 10
        self.speed = speed

        # Patrulha
        self.start_x = position[0]
        self.patrol_range = patrol_range
        self.direction = 1

    def move(self):
        # Movimento de patrulha
        self.rect.x += self.speed * self.direction
        if self.rect.x < self.start_x + self.patrol_range[0] or self.rect.x > self.start_x + self.patrol_range[1]:
            self.direction *= -1

        # ===== Animação =====
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.surf = self.frames[self.current_frame]

        if self.direction < 0:
            self.surf = pygame.transform.flip(self.surf, True, False)
