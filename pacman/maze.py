import pygame
from constants import *

class Maze:
    def __init__(self):
        self.layout = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W............WW............W",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
            "WoW  W.W   W.WW.W   W.W  WoW",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
            "W..........................W",
            "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
            "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
            "W......WW....WW....WW......W",
            "WWWWWW.WWWWW WW WWWWW.WWWWWW",
            "     W.WWWWW WW WWWWW.W     ",
            "     W.WW          WW.W     ",
            "     W.WW WWWWWWWW WW.W     ",
            "WWWWWW.WW W      W WW.WWWWWW",
            "      .   W      W   .      ",
            "WWWWWW.WW W      W WW.WWWWWW",
            "     W.WW WWWWWWWW WW.W     ",
            "     W.WW          WW.W     ",
            "     W.WW WWWWWWWW WW.W     ",
            "WWWWWW.WW WWWWWWWW WW.WWWWWW",
            "W............WW............W",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
            "Wo..WW.......  .......WW..oW",
            "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",
            "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",
            "W......WW....WW....WW......W",
            "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",
            "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",
            "W..........................W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        self.pellets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.create_maze_sprites()

    def create_maze_sprites(self):
        for row, line in enumerate(self.layout):
            for col, char in enumerate(line):
                if char == 'W':
                    Wall(self.walls, x=col * TILE_SIZE, y=row * TILE_SIZE)
                elif char == '.':
                    Pellet(self.pellets, x=col * TILE_SIZE + TILE_SIZE // 2, y=row * TILE_SIZE + TILE_SIZE // 2)
                elif char == 'o':
                    PowerPellet(self.pellets, x=col * TILE_SIZE + TILE_SIZE // 2, y=row * TILE_SIZE + TILE_SIZE // 2)

    def draw(self, screen):
        self.walls.draw(screen)
        self.pellets.draw(screen)

    def get_player_start_pos(self):
        return (14 * TILE_SIZE, 23 * TILE_SIZE)

    def get_ghost_start_pos(self):
        return (13 * TILE_SIZE, 11 * TILE_SIZE)

class Wall(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y):
        super().__init__(*groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

class Pellet(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y):
        super().__init__(*groups)
        self.image = pygame.Surface((4, 4))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

class PowerPellet(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y):
        super().__init__(*groups)
        self.image = pygame.Surface((8, 8))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))