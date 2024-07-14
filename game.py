import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 640
screen_height = 480
cell_size = 64

# Load the sprite image
sprite_sheet = pygame.image.load('snake_sprite.png')

# Extract images from the sprite sheet
def extract_sprite(x, y, width, height):
    image = pygame.Surface([width, height], pygame.SRCALPHA)
    image.blit(sprite_sheet, (0, 0), (x, y, width, height))
    return image

# Snake parts
head = extract_sprite(128, 0, 64, 64)
body = extract_sprite(128, 64, 64, 64)
tail = extract_sprite(0, 64, 64, 64)
corner = extract_sprite(64, 0, 64, 64)
food_image = extract_sprite(0, 0, 64, 64)

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.positions = [(100, 100)]
        self.direction = pygame.K_RIGHT
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]

        if self.direction == pygame.K_UP:
            new_head = (head_x, head_y - cell_size)
        elif self.direction == pygame.K_DOWN:
            new_head = (head_x, head_y + cell_size)
        elif self.direction == pygame.K_LEFT:
            new_head = (head_x - cell_size, head_y)
        elif self.direction == pygame.K_RIGHT:
            new_head = (head_x + cell_size, head_y)

        if self.grow:
            self.positions = [new_head] + self.positions
            self.grow = False
        else:
            self.positions = [new_head] + self.positions[:-1]

    def change_direction(self, direction):
        opposite_directions = {pygame.K_UP: pygame.K_DOWN, pygame.K_DOWN: pygame.K_UP, pygame.K_LEFT: pygame.K_RIGHT, pygame.K_RIGHT: pygame.K_LEFT}
        if direction != opposite_directions.get(self.direction):
            self.direction = direction

    def check_collision(self):
        head_x, head_y = self.positions[0]
        return (
            head_x < 0 or head_x >= screen_width or 
            head_y < 0 or head_y >= screen_height or 
            len(self.positions) != len(set(self.positions))
        )

    def grow_snake(self):
        self.grow = True

    def draw(self):
        for i, (x, y) in enumerate(self.positions):
            if i == 0:
                screen.blit(head, (x, y))
            elif i == len(self.positions) - 1:
                screen.blit(tail, (x, y))
            else:
                screen.blit(body, (x, y))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.new_position()

    def new_position(self):
        self.position = (
            random.randint(0, (screen_width - cell_size) // cell_size) * cell_size,
            random.randint(0, (screen_height - cell_size) // cell_size) * cell_size
        )

    def draw(self):
        screen.blit(food_image, self.position)

def main():
    snake = Snake()
    food = Food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)

        snake.move()
        
        if snake.positions[0] == food.position:
            snake.grow_snake()
            food.new_position()
            score += 1

        if snake.check_collision():
            pygame.quit()
            sys.exit()

        screen.fill(BLACK)
        snake.draw()
        food.draw()

        # Draw the score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    main()
