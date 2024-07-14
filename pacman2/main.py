# main.py
import pygame
import sys
from game import Game
from settings import Settings

def main():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    game = Game(screen, settings)

    while True:
        game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(settings.fps)

if __name__ == "__main__":
    main()
