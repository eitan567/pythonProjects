import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pac-Man')

# Maze layout (1 represents a wall, 0 represents a path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Pac-Man class
class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 'STOP'
        self.speed = GRID_SIZE // 4

    def can_move(self, direction):
        new_x, new_y = self.x, self.y
        if direction == 'UP':
            new_y -= self.speed
        elif direction == 'DOWN':
            new_y += self.speed
        elif direction == 'LEFT':
            new_x -= self.speed
        elif direction == 'RIGHT':
            new_x += self.speed

        new_x_grid = new_x // (GRID_SIZE-2)
        new_y_grid = new_y // (GRID_SIZE-3)

        if maze[new_y_grid][new_x_grid] == 0:
            return True
        return False

    def update(self):
        if self.direction == 'UP' and self.can_move('UP'):
            self.y -= self.speed
        elif self.direction == 'DOWN' and self.can_move('DOWN'):
            self.y += self.speed
        elif self.direction == 'LEFT' and self.can_move('LEFT'):
            self.x -= self.speed
        elif self.direction == 'RIGHT' and self.can_move('RIGHT'):
            self.x += self.speed

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 2)

# Create a Pac-Man instance
pacman = PacMan(GRID_SIZE, GRID_SIZE)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.direction = 'UP'
            elif event.key == pygame.K_DOWN:
                pacman.direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                pacman.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                pacman.direction = 'RIGHT'

    # Update Pac-Man
    pacman.update()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the maze
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw Pac-Man
    pacman.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
