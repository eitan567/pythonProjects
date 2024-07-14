# player.py
import pygame

class Player:
    def __init__(self, settings, maze):
        self.settings = settings
        self.maze = maze
        self.x = settings.cell_size * 1.5
        self.y = settings.cell_size * 1.5
        self.direction = (0, 0)
        self.image = pygame.Surface((settings.cell_size, settings.cell_size))
        self.image.fill((255, 255, 0))  # Yellow for Pac-Man

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                self.direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                self.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.direction = (1, 0)

    def update(self):
        new_x = self.x + self.direction[0] * self.settings.pacman_speed
        new_y = self.y + self.direction[1] * self.settings.pacman_speed
        if self.maze.is_valid_position(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
