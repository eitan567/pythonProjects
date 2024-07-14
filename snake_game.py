import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
SCOREBOARD_HEIGHT = 40
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - SCOREBOARD_HEIGHT) // GRID_SIZE
FPS_SNAKE = 60
LIVES = 3
APPLE_ANIMATION_SPEED = 5  # Frames per image change
BANANA_ANIMATION_SPEED = 5  # Frames per image change

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Load images
HEAD_IMAGES = {
    'UP': pygame.image.load('images/snake/head_up.gif'),
    'DOWN': pygame.image.load('images/snake/head_down.gif'),
    'LEFT': pygame.image.load('images/snake/head_left.gif'),
    'RIGHT': pygame.image.load('images/snake/head_right.gif')
}
TAIL_IMAGES = {
    'UP': pygame.image.load('images/snake/tail_up.gif'),
    'DOWN': pygame.image.load('images/snake/tail_down.gif'),
    'LEFT': pygame.image.load('images/snake/tail_left.gif'),
    'RIGHT': pygame.image.load('images/snake/tail_right.gif')
}
BODY_IMAGES = {
    'HORIZONTAL': pygame.image.load('images/snake/body_horizontal.gif'),
    'VERTICAL': pygame.image.load('images/snake/body_vertical.gif'),
    'CURVE_UP_RIGHT': pygame.image.load('images/snake/body_curve_up_right.gif'),
    'CURVE_UP_LEFT': pygame.image.load('images/snake/body_curve_up_left.gif'),
    'CURVE_DOWN_RIGHT': pygame.image.load('images/snake/body_curve_down_right.gif'),
    'CURVE_DOWN_LEFT': pygame.image.load('images/snake/body_curve_down_left.gif')
}
APPLE_IMAGES = [pygame.image.load(f'images/heart/heart-{i}.png') for i in range(1, 19)]
BANANA_IMAGES = [pygame.image.load(f'images/star/star{i}.png') for i in range(1, 7)]

# Scale images
for key in HEAD_IMAGES:
    HEAD_IMAGES[key] = pygame.transform.scale(HEAD_IMAGES[key], (GRID_SIZE, GRID_SIZE))
for key in TAIL_IMAGES:
    TAIL_IMAGES[key] = pygame.transform.scale(TAIL_IMAGES[key], (GRID_SIZE, GRID_SIZE))
for key in BODY_IMAGES:
    BODY_IMAGES[key] = pygame.transform.scale(BODY_IMAGES[key], (GRID_SIZE, GRID_SIZE))
APPLE_IMAGES = [pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE)) for img in APPLE_IMAGES]
BANANA_IMAGES = [pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE)) for img in BANANA_IMAGES]

# Load sounds
MOVE_SOUND = pygame.mixer.Sound('sfx/move.mp3')
EAT_SOUND = pygame.mixer.Sound('sfx/gamestart.mp3')
GAMEOVER_SOUND = pygame.mixer.Sound('sfx/game-over-classic.mp3')
BONUS_SOUND = pygame.mixer.Sound('sfx/bonus.mp3')
BACKGROUND_MUSIC = 'sfx/game-music-loop-6.mp3'

# Set volume for sounds
MOVE_SOUND.set_volume(0.5)  # 50% volume
EAT_SOUND.set_volume(0.7)   # 70% volume
GAMEOVER_SOUND.set_volume(1.0)  # 100% volume
BONUS_SOUND.set_volume(0.7)  # 70% volume
pygame.mixer.music.set_volume(0.3)  # 30% volume

# Initialize channels for different sounds
MOVE_CHANNEL = pygame.mixer.Channel(0)
EAT_CHANNEL = pygame.mixer.Channel(1)
GAMEOVER_CHANNEL = pygame.mixer.Channel(2)
BONUS_CHANNEL = pygame.mixer.Channel(3)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Fireball class
class Fireball:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.active = True

    def move(self):
        if self.active:
            self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
            if (self.position[0] < 0 or self.position[0] >= GRID_WIDTH or
                self.position[1] < 0 or self.position[1] >= GRID_HEIGHT):
                self.active = False

    def draw(self, screen):
        if self.active:
            screen_x = self.position[0] * GRID_SIZE
            screen_y = self.position[1] * GRID_SIZE + SCOREBOARD_HEIGHT
            pygame.draw.circle(screen, ORANGE, (screen_x + GRID_SIZE // 2, screen_y + GRID_SIZE // 2), GRID_SIZE // 2)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Play background music
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(-1)  # Play the music in a loop

def save_score(score):
    with open('scores.txt', 'a') as file:
        file.write(f'{score}\n')

def load_scores():
    try:
        with open('scores.txt', 'r') as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return []

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, SCOREBOARD_HEIGHT), (x, HEIGHT))
    for y in range(SCOREBOARD_HEIGHT, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def get_direction(segment, next_segment):
    if segment[0] == next_segment[0]:  # Vertical movement
        if segment[1] > next_segment[1]:
            return 'UP'
        else:
            return 'DOWN'
    else:  # Horizontal movement
        if segment[0] > next_segment[0]:
            return 'LEFT'
        else:
            return 'RIGHT'

def get_curve(segment, next_segment):
    if segment[0] < next_segment[0] and segment[1] > next_segment[1]:
        return 'CURVE_DOWN_LEFT'
    elif segment[0] < next_segment[0] and segment[1] < next_segment[1]:
        return 'CURVE_UP_LEFT'
    elif segment[0] > next_segment[0] and segment[1] > next_segment[1]:
        return 'CURVE_DOWN_RIGHT'
    elif segment[0] > next_segment[0] and segment[1] < next_segment[1]:
        return 'CURVE_UP_RIGHT'
    return None

def draw_snake(snake):
    for i, segment in enumerate(snake):
        screen_x = segment[0] * GRID_SIZE
        screen_y = segment[1] * GRID_SIZE + SCOREBOARD_HEIGHT
        if i == 0:  # Head
            if len(snake) > 1:
                direction = get_direction(segment, snake[1])
            else:
                direction = 'RIGHT'  # Default direction if snake has only one segment
            screen.blit(HEAD_IMAGES[direction], (screen_x, screen_y))
        elif i == len(snake) - 1:  # Tail
            direction = get_direction(snake[i - 1], segment)
            screen.blit(TAIL_IMAGES[direction], (screen_x, screen_y))
        else:  # Body
            if segment[0] == snake[i - 1][0] and segment[0] == snake[i + 1][0]:
                screen.blit(BODY_IMAGES['VERTICAL'], (screen_x, screen_y))
            elif segment[1] == snake[i - 1][1] and segment[1] == snake[i + 1][1]:
                screen.blit(BODY_IMAGES['HORIZONTAL'], (screen_x, screen_y))
            else:
                curve = get_curve(snake[i - 1], segment, snake[i + 1])
                screen.blit(BODY_IMAGES[curve], (screen_x, screen_y))

def get_curve(prev_segment, current_segment, next_segment):
    dx1 = current_segment[0] - prev_segment[0]
    dy1 = current_segment[1] - prev_segment[1]
    dx2 = next_segment[0] - current_segment[0]
    dy2 = next_segment[1] - current_segment[1]

    if dx1 == 0 and dy2 == 0:  # Turn from vertical to horizontal
        return 'CURVE_UP_RIGHT' if dy1 < 0 else 'CURVE_DOWN_RIGHT'
    elif dy1 == 0 and dx2 == 0:  # Turn from horizontal to vertical
        return 'CURVE_UP_LEFT' if dx1 < 0 else 'CURVE_UP_RIGHT'
    elif dx1 == 0 and dy2 == 0:  # Turn from vertical to horizontal
        return 'CURVE_UP_LEFT' if dy1 < 0 else 'CURVE_DOWN_LEFT'
    else:  # Turn from horizontal to vertical
        return 'CURVE_DOWN_LEFT' if dx1 < 0 else 'CURVE_DOWN_RIGHT'

def reset_game():
    direction = RIGHT
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    banana = None
    banana_timer = random.randint(10, 30)  # Random time between 10 and 30 seconds for the banana to appear
    fireballs = []
    return direction, snake, food, banana, banana_timer, fireballs

def main():
    direction, snake, food, banana, banana_timer, fireballs = reset_game()
    score = 0
    highest_score = 0
    lives = LIVES
    scores = load_scores()
    last_banana_time = time.time()
    banana_start_time = None
    fireball_tick_counter = 0
    apple_frame = 0
    banana_frame = 0
    apple_timer = 0
    banana_timer = 0

    while True:
        while lives > 0:
            current_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_UP and direction != DOWN:
                        direction = UP
                    elif event.key == pygame.K_DOWN and direction != UP:
                        direction = DOWN
                    elif event.key == pygame.K_LEFT and direction != RIGHT:
                        direction = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        direction = RIGHT
                    elif event.key == pygame.K_SPACE:  # Fire a fireball
                        fireball_position = snake[0]
                        fireball_direction = direction
                        fireballs.append(Fireball(fireball_position, fireball_direction))

            # Move snake
            if fireball_tick_counter % 10 == 0:
                new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
                snake.insert(0, new_head)

                # Play move sound
                MOVE_CHANNEL.play(MOVE_SOUND)

                # Check for food
                if snake[0] == food:
                    score += 1
                    EAT_CHANNEL.play(EAT_SOUND)
                    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                else:
                    snake.pop()

                # Check for collisions
                if (snake[0][0] < 0 or snake[0][0] >= GRID_WIDTH or
                    snake[0][1] < 0 or snake[0][1] >= GRID_HEIGHT or
                    snake[0] in snake[1:]):
                    lives -= 1
                    if lives > 0:
                        direction, snake, food, banana, banana_timer, fireballs = reset_game()
                    highest_score = max(highest_score, score)

            # Check for banana
            if banana:
                if snake[0] == banana:
                    score += 10
                    BONUS_CHANNEL.play(BONUS_SOUND)
                    banana = None
                    banana_timer = random.randint(10, 30)
                    banana_start_time = None
                elif current_time - banana_start_time > 4:
                    banana = None
                    banana_start_time = None

            # Move fireballs
            fireball_tick_counter += 1
            if fireball_tick_counter % 4 == 0:
                for fireball in fireballs:
                    fireball.move()
                    if fireball.position == food:
                        score += 1
                        EAT_CHANNEL.play(EAT_SOUND)
                        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                        fireball.active = False
                    if fireball.position == banana:
                        score += 10
                        BONUS_CHANNEL.play(BONUS_SOUND)
                        banana = None
                        banana_timer = random.randint(10, 30)
                        banana_start_time = None
                        fireball.active = False

                fireballs = [fireball for fireball in fireballs if fireball.active]

            # Animate apple
            apple_timer += 1
            if apple_timer >= APPLE_ANIMATION_SPEED:
                apple_frame = (apple_frame + 1) % len(APPLE_IMAGES)
                apple_timer = 0

            # Animate banana
            if banana:
                banana_timer += 1
                if banana_timer >= BANANA_ANIMATION_SPEED:
                    banana_frame = (banana_frame + 1) % len(BANANA_IMAGES)
                    banana_timer = 0

            # Spawn banana at random intervals
            if not banana and current_time - last_banana_time >= banana_timer:
                banana = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                last_banana_time = current_time
                banana_start_time = current_time

            # Draw everything
            screen.fill(WHITE)
            draw_grid()
            draw_snake(snake)
            screen.blit(APPLE_IMAGES[apple_frame], (food[0] * GRID_SIZE, food[1] * GRID_SIZE + SCOREBOARD_HEIGHT))
            if banana:
                screen.blit(BANANA_IMAGES[banana_frame], (banana[0] * GRID_SIZE, banana[1] * GRID_SIZE + SCOREBOARD_HEIGHT))
                remaining_time = 4 - int(current_time - banana_start_time)
                font = pygame.font.Font(None, 36)
                countdown_text = font.render(str(remaining_time), True, RED)
                screen.blit(countdown_text, (banana[0] * GRID_SIZE + 10, banana[1] * GRID_SIZE + SCOREBOARD_HEIGHT + 10))
            for fireball in fireballs:
                fireball.draw(screen)
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {score}', True, BLACK)
            lives_text = font.render(f'Lives: {lives}', True, BLACK)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (WIDTH - 100, 10))
            pygame.display.flip()

            clock.tick(FPS_SNAKE)

        # Play game over sound
        GAMEOVER_CHANNEL.play(GAMEOVER_SOUND)

        # Game over
        save_score(score)
        scores.append(score)
        scores.sort(reverse=True)
        scores = scores[:3]  # Keep top 3 scores

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        direction, snake, food, banana, banana_timer, fireballs = reset_game()
                        score = 0  # Reset score for the new session
                        lives = LIVES
                        break

            else:
                screen.fill(WHITE)
                font = pygame.font.Font(None, 36)
                game_over_text = font.render('Game Over', True, BLACK)
                score_text = font.render(f'Your Score: {highest_score}', True, BLACK)
                new_game_text = font.render('Press Enter to start a new game', True, BLACK)
                quit_game_text = font.render('Press Esc to quit', True, BLACK)
                screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 6 - 50))
                screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 6))
                screen.blit(new_game_text, (WIDTH // 2 - 200, HEIGHT // 6 + 100))
                screen.blit(quit_game_text, (WIDTH // 2 - 200, HEIGHT // 6 + 150))

                y_offset = 200
                for i, score in enumerate(scores):
                    score_text = font.render(f'{i + 1}. {score}', True, BLACK)
                    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 6 + y_offset))
                    y_offset += 40

                pygame.display.flip()
                clock.tick(FPS_SNAKE)
                continue
            break

if __name__ == '__main__':
    main()
