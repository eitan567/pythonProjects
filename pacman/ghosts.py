# ghosts.py

import pygame
import random
from constants import *

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.speed = 1

    def move(self, walls):
        new_pos = self.rect.move(self.direction * self.speed)
        if not self.check_collision(new_pos, walls):
            self.rect = new_pos
        else:
            self.change_direction(walls)

        # Wrap around the screen
        self.rect.x %= SCREEN_WIDTH
        self.rect.y %= SCREEN_HEIGHT

    def check_collision(self, pos, walls):
        temp_rect = self.rect.copy()
        temp_rect.topleft = pos.topleft
        return any(temp_rect.colliderect(wall.rect) for wall in walls)

    def change_direction(self, walls):
        possible_directions = [UP, DOWN, LEFT, RIGHT]
        random.shuffle(possible_directions)
        
        for direction in possible_directions:
            new_pos = self.rect.move(direction * self.speed)
            if not self.check_collision(new_pos, walls):
                self.direction = direction
                break

    def update(self, walls):
        self.move(walls)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, RED)

class Pinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, PINK)

class Inky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, CYAN)

class Clyde(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, ORANGE)