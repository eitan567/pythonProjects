# main.py

import pygame
import sys
from constants import *
from maze import Maze
from player import Player
from ghosts import Blinky, Pinky, Inky, Clyde

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.maze = Maze()
        player_start = self.maze.get_player_start_pos()
        ghost_start = self.maze.get_ghost_start_pos()
        self.player = Player(*player_start)
        
        # Updated ghost starting positions
        self.ghosts = pygame.sprite.Group(
            Blinky(ghost_start[0] - TILE_SIZE, ghost_start[1] - TILE_SIZE),
            Pinky(ghost_start[0] + TILE_SIZE, ghost_start[1] - TILE_SIZE),
            Inky(ghost_start[0] - TILE_SIZE, ghost_start[1] + TILE_SIZE),
            Clyde(ghost_start[0] + TILE_SIZE, ghost_start[1] + TILE_SIZE)
        )
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.change_direction(UP)
        elif keys[pygame.K_DOWN]:
            self.player.change_direction(DOWN)
        elif keys[pygame.K_LEFT]:
            self.player.change_direction(LEFT)
        elif keys[pygame.K_RIGHT]:
            self.player.change_direction(RIGHT)
        
        return True

    def update(self):
        self.player.update(self.maze.walls)
        for ghost in self.ghosts:
            ghost.update(self.maze.walls)

        # Wrap around the screen for the player
        self.player.rect.x %= SCREEN_WIDTH
        self.player.rect.y %= SCREEN_HEIGHT

        # Check for pellet collisions
        pellets_collected = pygame.sprite.spritecollide(self.player, self.maze.pellets, True)
        self.score += len(pellets_collected)

        # Check for ghost collisions
        if pygame.sprite.spritecollide(self.player, self.ghosts, False):
            print("Game Over!")
            return False

        return True

    def draw(self):
        self.screen.fill(BLACK)
        self.maze.draw(self.screen)
        self.player.draw(self.screen)
        self.ghosts.draw(self.screen)
        self.draw_score()
        pygame.display.flip()

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            if running:
                running = self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()