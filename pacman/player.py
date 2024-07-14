import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = pygame.Vector2(0, 0)
        self.speed = 2
        self.next_direction = None

    def move(self, walls):
        if self.next_direction:
            next_pos = self.rect.move(self.next_direction * self.speed)
            if not self.check_collision(next_pos, walls):
                self.direction = self.next_direction
                self.next_direction = None

        new_pos = self.rect.move(self.direction * self.speed)
        if not self.check_collision(new_pos, walls):
            self.rect = new_pos

    def check_collision(self, pos, walls):
        temp_rect = self.rect.copy()
        temp_rect.topleft = pos.topleft
        return any(temp_rect.colliderect(wall.rect) for wall in walls)

    def change_direction(self, new_direction):
        self.next_direction = new_direction

    def update(self, walls):
        self.move(walls)

    def draw(self, screen):
        screen.blit(self.image, self.rect)