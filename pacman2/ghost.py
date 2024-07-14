# ghost.py
import pygame
import random

class Ghost:
    def __init__(self, settings, maze):
        self.settings = settings
        self.maze = maze
        self.x = settings.cell_size * 9.5
        self.y = settings.cell_size * 9.5
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.image = pygame.Surface((settings.cell_size, settings.cell_size))
        self.image.fill((255, 0, 0))  # Red for Ghost

    def update(self):
        new_x = self.x + self.direction[0] * self.settings.ghost_speed
        new_y = self.y + self.direction[1] * self.settings.ghost_speed
        if self.maze.is_valid_position(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
