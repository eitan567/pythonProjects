import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# Snake settings
snake_block = 10
snake_speed = 15

# Font for the scoreboard
font_style = pygame.font.SysFont(None, 50)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 3, height / 3])

# Game loop
clock = pygame.time.Clock()
snake_list = []
length_of_snake = 1
x1 = width / 2
y1 = height / 2
x1_change = 0
y1_change = 0

foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -snake_block
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = snake_block
                x1_change = 0
    
    # Update the position of the snake's head
    x1 += x1_change
    y1 += y1_change
    
    # Check for boundaries
    if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
        game_close = True
        pygame.quit()
        sys.exit()
    
    # Update snake list
    snake_head = []
    snake_head.append(x1)
    snake_head.append(y1)
    snake_list.append(snake_head)
    
    if len(snake_list) > length_of_snake:
        del snake_list[0]
    
    # Check for collision with the food
    if x1 == foodx and y1 == foody:
        foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
        length_of_snake += 1
    
    # Draw the background and the snake
    screen.fill(black)
    for body in snake_list[:-1]:
        pygame.draw.rect(screen, green, [body[0], body[1], snake_block, snake_block])
    our_snake(snake_block, snake_list)
    
    # Draw the food
    pygame.draw.rect(screen, red, [int(foodx), int(foody), snake_block, snake_block])
    
    # Update the scoreboard
    score = font_style.render("Score: " + str(length_of_snake - 1), True, white)
    screen.blit(score, [0, 0])
    
    pygame.display.update()
    
    clock.tick(snake_speed)

pygame.quit()
sys.exit()