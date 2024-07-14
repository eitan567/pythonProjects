import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 54, 66)
green = (0, 255, 0)
blue = (52, 152, 219)

dis_width = 800
dis_height  = 600

snake_block = 10
dis_thickness = 3

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
scoreboard_font = pygame.font.SysFont("comicsansms", 35)

gameDisplay = pygame.display.set_mode((dis_width, dis_height))
pygame.display.flip()       

def drawGrid(screen):
    for i in range(1, 40):
        if i % 5 == 0:
            pygame.draw.line(screen, black, [0, i * snake_block], [dis_width, i * snake_block])
        else:
            pygame.draw.line(screen, gray, [0, i * snake_block], [dis_width, i * snake_block], 1)

    pygame.display.update()

def text_score(text, color, x, y):
    label = font_style.render(text, True, color)
    gameDisplay.blit(label, (x, y))
    
def score(points):
    return scoreboard_font.render("Score: " + str(points), True, blue)
    
def snake(snake_block):
    disp_width = dis_width - 20
    disp_height = dis_height - 25
    for block in snake_block:
        pygame.draw.rect(gameDisplay, black, [block[0]*snake_block, block[1]*snake_block, snake_block, snake_block])
        
def message():
    mensong = scoreboard_font.render("Game Over!", True, red)
    gameDisplay.blit(mensong, [dis_width/2 - 30, dis_height/2 -50])
    
def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = dis_width / 2
    lead_y = dis_height / 2
    block_size = snake_block
    space = 10
    direction = 'RIGHT'
    
    clock.tick(5)
    font = pygame.font.SysFont("comicsansms", 60)
    scoreboard_value = 0
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            
        if direction == 'RIGHT':
            lead_x += space
        elif direction == 'LEFT':
            lead_x -= space
        elif direction == 'DOWN':
            lead_y += space
        elif direction == 'UP':
            lead_y -= space
        
        gameDisplay.fill(white)
        
        if lead_x < 0:
            lead_x = 0
            
        elif lead_x > dis_width - snake_block:
            lead_x = dis_width - snake_block
            
        if lead_y < 0:
            lead_y = 0
        
        elif lead_y > dis_height - snake_block:
            lead_y = dis_height - snake_block
        
        gameDisplay.fill((255, 255, 255))
        pygame.draw.rect(gameDisplay, blue, [lead_x, lead_y, block_size, block_size])
        
        for i in snake_block:
            if lead_x == i[0] and lead_y == i[1]:
                gameOver = True
            
        text_score(str(scoreboard_value), green, 10, 10)
        
        pygame.display.update()
        
        if gameOver:
            message()
            font = pygame.font.SysFont("comicsansms", 45)
            text = font.render('Press a key to restart', True, blue)
            gameDisplay.blit(text, [dis_width/2 - 100, dis_height/2 + 50])
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                direction = 'LEFT'
                
            elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                direction = 'RIGHT'
            
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                direction = 'DOWN'
                
            elif event.key == pygame.K_UP or event.key == ord('w'):
                direction = 'UP'
        
        if not gameOver:
            snake(snake_block)
            
        scoreboard_value += 1
    
    pygame.quit()
    quit()
gameLoop()