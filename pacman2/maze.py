# maze.py
import pygame

class Maze:
    def __init__(self, settings):
        self.settings = settings
        self.layout = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def draw(self, screen):
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, (0, 0, 255),
                                     (x * self.settings.cell_size,
                                      y * self.settings.cell_size,
                                      self.settings.cell_size,
                                      self.settings.cell_size))

    def is_valid_position(self, x, y):
        grid_x = int(x // self.settings.cell_size)
        grid_y = int(y // self.settings.cell_size)
        return (0 <= grid_x < len(self.layout[0]) and
                0 <= grid_y < len(self.layout) and
                self.layout[grid_y][grid_x] == 0)
