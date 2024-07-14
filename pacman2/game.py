# game.py
import pygame
from player import Player
from ghost import Ghost
from maze import Maze

class Game:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.maze = Maze(settings)
        self.player = Player(settings, self.maze)
        self.ghosts = [Ghost(settings, self.maze) for _ in range(4)]
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.player.handle_event(event)

    def update(self):
        self.player.update()
        for ghost in self.ghosts:
            ghost.update()
        self.check_collisions()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)
        self.player.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        self.draw_score()

    def check_collisions(self):
        # Implement collision detection here
        pass

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
