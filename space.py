# Web initialization block for pygbag
import sys

if sys.platform == "emscripten":
    import asyncio
    import pygame
    from pygame.locals import *

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Your original imports
import pygame
import random
import os

def main():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Set up the game window
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    # Player
    player_width = 50
    player_height = 50
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 10
    player_speed = 5

    # Load player spaceship image
    player_image = pygame.image.load(os.path.join("images/aliens", "alien-13.png"))
    player_image = pygame.transform.scale(player_image, (player_width, player_height))

    # Load explosion animation frames
    explosion_frames = []
    for i in range(1, 10):  # Assuming you have 9 frames of explosion animation
        frame = pygame.image.load(os.path.join("images/explosion", f"explosion{i}.png"))
        explosion_frames.append(pygame.transform.scale(frame, (player_width, player_height)))

    # Load player death sound
    player_death_sound = pygame.mixer.Sound('sfx/player-death.mp3')
    player_death_sound.set_volume(0.5)

    # Bullets
    bullet_width = 5
    bullet_height = 15
    bullet_speed = 7
    bullets = []

    # Alien bullets
    alien_bullet_width = 5
    alien_bullet_height = 15
    alien_bullet_speed = 5
    alien_bullets = []

    # Game variables
    score = 0
    lives = 3
    level = 1
    font = pygame.font.Font(None, 36)

    # Sound channels
    pygame.mixer.set_num_channels(5)
    channel_bg = pygame.mixer.Channel(0)
    channel_shoot = pygame.mixer.Channel(1)
    channel_alien = pygame.mixer.Channel(2)
    channel_alien_shoot = pygame.mixer.Channel(3)

    # Load sound effects
    shoot_sound = pygame.mixer.Sound('sfx/shoot.mp3')
    alien_death_sound = pygame.mixer.Sound('sfx/alien-death.mp3')
    background_music = pygame.mixer.Sound('sfx/alien-invasion-music.mp3')
    alien_shoot_sound = pygame.mixer.Sound('sfx/shoot.mp3')

    # Set volumes
    shoot_sound.set_volume(0.1)
    alien_death_sound.set_volume(0.3)
    background_music.set_volume(0.7)
    alien_shoot_sound.set_volume(0.1)

    # Play background music
    channel_bg.play(background_music, loops=-1)

    # Load alien images
    alien_images = []
    for file in os.listdir("images/aliens"):
        if file.endswith(".png"):
            img = pygame.image.load(os.path.join("images/aliens", file))
            alien_images.append(pygame.transform.scale(img, (50, 50)))

    class Enemy:
        def __init__(self, x, y, image):
            self.rect = pygame.Rect(x, y, 50, 50)
            self.image = image

    def create_enemies(level):
        enemies = []
        rows = 3 + level
        cols = 8 + level
        enemy_width = 50
        enemy_height = 50
        
        if len(alien_images) < rows:
            raise ValueError("Not enough unique alien images for the current level")
        
        selected_images = random.sample(alien_images, rows)
        
        for j in range(rows):
            row_image = selected_images[j]
            for i in range(cols):
                enemy = Enemy(i * (enemy_width + 10), j * (enemy_height + 10) + 50, row_image)
                enemies.append(enemy)
        return enemies

    def next_level():
        global level, enemies, enemy_speed
        level += 1
        if level > 3:
            game_over("You Win!")
        else:
            enemies = create_enemies(level)
            enemy_speed = 2 + level

    def game_over(message):
        global running
        screen.fill(BLACK)
        game_over_text = font.render(message, True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    def player_death_animation(x, y):
        for frame in explosion_frames:
            screen.fill(BLACK)
            screen.blit(frame, (x, y))
            pygame.display.flip()
            pygame.time.wait(100)
        player_death_sound.play()

    # Initial setup
    enemies = create_enemies(level)
    enemy_speed = 2 + level

    # Game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height))
                    channel_shoot.play(shoot_sound)

        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Move enemies
        move_down = False
        for enemy in enemies:
            enemy.rect.x += enemy_speed
            if enemy.rect.right > WIDTH or enemy.rect.left < 0:
                move_down = True
        
        if move_down:
            enemy_speed = -enemy_speed
            for enemy in enemies:
                enemy.rect.y += 10
                if enemy.rect.bottom >= player_y:
                    game_over("Game Over! Aliens reached your ship.")
                    break

        # Alien shooting
        if random.randint(1, 100) == 1 and enemies:  # 1% chance each frame
            shooting_alien = random.choice(enemies)
            alien_bullets.append(pygame.Rect(
                shooting_alien.rect.centerx - alien_bullet_width // 2,
                shooting_alien.rect.bottom,
                alien_bullet_width,
                alien_bullet_height
            ))
            channel_alien_shoot.play(alien_shoot_sound)

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move alien bullets
        for bullet in alien_bullets[:]:
            bullet.y += alien_bullet_speed
            if bullet.top > HEIGHT:
                alien_bullets.remove(bullet)

        # Check for collisions
        enemies_to_remove = []
        bullets_to_remove = []
        for i, enemy in enumerate(enemies):
            for j, bullet in enumerate(bullets):
                if enemy.rect.colliderect(bullet):
                    enemies_to_remove.append(i)
                    bullets_to_remove.append(j)
                    score += 10
                    channel_alien.play(alien_death_sound)

        # Remove enemies and bullets
        for index in sorted(enemies_to_remove, reverse=True):
            enemies.pop(index)
        for index in sorted(bullets_to_remove, reverse=True):
            bullets.pop(index)

        # Check for player collision with alien bullets
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for bullet in alien_bullets[:]:
            if player_rect.colliderect(bullet):
                alien_bullets.remove(bullet)
                lives -= 1
                player_death_animation(player_x, player_y)
                if lives <= 0:
                    game_over("Game Over! You ran out of lives.")

        # Check if all enemies are defeated
        if len(enemies) == 0:
            next_level()

        # Draw everything
        screen.fill(BLACK)
        screen.blit(player_image, (player_x, player_y))
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)
        for bullet in bullets:
            pygame.draw.rect(screen, BLUE, bullet)
        for bullet in alien_bullets:
            pygame.draw.rect(screen, RED, bullet)

        # Draw score, lives, and level
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))
        screen.blit(level_text, (WIDTH // 2 - 50, 10))

        pygame.display.flip()
        clock.tick(60)

    # Stop all sounds and quit
    pygame.mixer.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
