import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doom-like Game with Visible Bullets")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Player settings
player_x, player_y = 1.5, 1.5
player_angle = 0
FOV = math.pi / 3
HALF_FOV = FOV / 2
mouse_sensitivity = 0.002

# Map
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

MAP_SIZE = len(MAP)
TILE_SIZE = (WIDTH // MAP_SIZE) // 3

# Monster
class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100

monsters = [Monster(3.5, 3.5), Monster(7.5, 5.5), Monster(12.5, 2.5)]

# Bullet
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0.2
        self.lifetime = 100

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.lifetime -= 1

    def check_collision(self):
        if MAP[int(self.y)][int(self.x)] == 1:
            return True
        for monster in monsters:
            if math.sqrt((self.x - monster.x)**2 + (self.y - monster.y)**2) < 0.5:
                monster.health -= 50
                if monster.health <= 0:
                    monsters.remove(monster)
                return True
        return False

bullets = []

# Load gun image
gun_image = pygame.image.load("images/gun.gif")
gun_image = pygame.transform.scale(gun_image, (200, 200))
gun_rect = gun_image.get_rect(center=(HALF_WIDTH, HEIGHT - 100))

# Gun settings
gun_rotation_speed = 0.05
gun_angle = 0

# Update these values based on your gun.gif image
GUN_TIP_OFFSET_X = 100  # Pixels from gun center to tip, horizontally
GUN_TIP_OFFSET_Y = -50  # Pixels from gun center to tip, vertically (negative if tip is above center)

def draw_gun():
    screen.blit(gun_image, gun_rect.topleft)

# Raycasting
def cast_ray(angle):
    epsilon = 1e-6
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    
    # Vertical grid line checks
    x_vert, dx = (math.floor(player_x) + 1, 1) if cos_a > 0 else (math.ceil(player_x) - 1, -1)
    depth_vert = (x_vert - player_x) / (cos_a + epsilon)
    y_vert = player_y + depth_vert * sin_a
    
    delta_depth = dx / (cos_a + epsilon)
    dy = delta_depth * sin_a
    
    for _ in range(20):
        tile_vert = int(x_vert), int(y_vert)
        if tile_vert[1] < 0 or tile_vert[1] >= len(MAP) or tile_vert[0] < 0 or tile_vert[0] >= len(MAP[0]) or MAP[tile_vert[1]][tile_vert[0]] == 1:
            break
        x_vert += dx
        y_vert += dy
        depth_vert += delta_depth
    
    # Horizontal grid line checks
    y_hor, dy = (math.floor(player_y) + 1, 1) if sin_a > 0 else (math.ceil(player_y) - 1, -1)
    depth_hor = (y_hor - player_y) / (sin_a + epsilon)
    x_hor = player_x + depth_hor * cos_a
    
    delta_depth = dy / (sin_a + epsilon)
    dx = delta_depth * cos_a
    
    for _ in range(20):
        tile_hor = int(x_hor), int(y_hor)
        if tile_hor[1] < 0 or tile_hor[1] >= len(MAP) or tile_hor[0] < 0 or tile_hor[0] >= len(MAP[0]) or MAP[tile_hor[1]][tile_hor[0]] == 1:
            break
        x_hor += dx
        y_hor += dy
        depth_hor += delta_depth
    
    # Choose the shorter distance
    if depth_vert < depth_hor:
        return depth_vert
    else:
        return depth_hor

# Drawing
def draw_world():
    screen.fill(BLACK)
    for x in range(WIDTH):
        angle = player_angle - HALF_FOV + (x / WIDTH) * FOV
        depth = cast_ray(angle)
        
        # Fix fish-eye effect
        depth *= math.cos(player_angle - angle)
        
        # Calculate wall height
        wall_height = min(int((HEIGHT * 0.75) / depth), HEIGHT)
        color_intensity = min(255, int(255 / (depth + 1)))
        wall_color = (color_intensity, color_intensity, color_intensity)
        
        # Draw wall slice
        start_y = HALF_HEIGHT - wall_height // 2
        end_y = start_y + wall_height
        pygame.draw.line(screen, wall_color, (x, start_y), (x, end_y))

    # Draw bullets in 3D view
    for bullet in bullets:
        bullet_angle = math.atan2(bullet.y - player_y, bullet.x - player_x) - player_angle
        bullet_dist = math.sqrt((bullet.x - player_x)**2 + (bullet.y - player_y)**2)
        
        # Check if bullet is in player's FOV
        if -HALF_FOV < bullet_angle < HALF_FOV:
            # Project bullet onto screen
            bullet_size = int(5 / bullet_dist)  # Size based on distance
            proj_x = HALF_WIDTH + math.tan(bullet_angle) * HALF_WIDTH
            proj_y = HALF_HEIGHT - (HEIGHT * 0.375) / bullet_dist
            pygame.draw.circle(screen, YELLOW, (int(proj_x), int(proj_y)), max(1, bullet_size))

def draw_minimap():
    mini_map_size = TILE_SIZE * MAP_SIZE
    mini_map = pygame.Surface((mini_map_size, mini_map_size))
    mini_map.fill(BLACK)
    
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile:
                pygame.draw.rect(mini_map, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
    
    # Center player in minimap
    center_x = mini_map_size // 2
    center_y = mini_map_size // 2

    # Draw player
    pygame.draw.circle(mini_map, RED, (center_x, center_y), 5)

    # Draw monsters
    for monster in monsters:
        mini_monster_x = center_x + int((monster.x - player_x) * TILE_SIZE)
        mini_monster_y = center_y + int((monster.y - player_y) * TILE_SIZE)
        pygame.draw.circle(mini_map, GREEN, (mini_monster_x, mini_monster_y), 3)
    
    # Draw bullets
    for bullet in bullets:
        mini_bullet_x = center_x + int((bullet.x - player_x) * TILE_SIZE)
        mini_bullet_y = center_y + int((bullet.y - player_y) * TILE_SIZE)
        pygame.draw.circle(mini_map, YELLOW, (mini_bullet_x, mini_bullet_y), 2)
    
    # Rotate minimap to align with player angle
    rotated_map = pygame.transform.rotate(mini_map, -math.degrees(player_angle))
    rotated_rect = rotated_map.get_rect(center=(WIDTH - mini_map_size // 2 - 10, HEIGHT - mini_map_size // 2 - 10))
    screen.blit(rotated_map, rotated_rect.topleft)

def screen_to_world(screen_x, screen_y):
    # Convert screen coordinates to world coordinates
    dx = (screen_x - HALF_WIDTH) / (WIDTH * 0.75)
    dy = (HALF_HEIGHT - screen_y) / (HEIGHT * 0.75)
    
    world_x = player_x + (dx * math.cos(player_angle) - dy * math.sin(player_angle))
    world_y = player_y + (dx * math.sin(player_angle) + dy * math.cos(player_angle))
    
    return world_x, world_y

# Game loop
clock = pygame.time.Clock()
running = True
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Shooting logic
            bullet_spawn_distance = 0.1  # Distance in front of the player to spawn the bullet
            spawn_x = player_x + bullet_spawn_distance * math.cos(player_angle)
            spawn_y = player_y + bullet_spawn_distance * math.sin(player_angle)
            
            bullets.append(Bullet(spawn_x, spawn_y, player_angle))
    
    # Movement and gun control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        new_x = player_x + 0.1 * math.cos(player_angle)
        new_y = player_y + 0.1 * math.sin(player_angle)
        if MAP[int(new_y)][int(new_x)] == 0:
            player_x, player_y = new_x, new_y
    if keys[pygame.K_DOWN]:
        new_x = player_x - 0.1 * math.cos(player_angle)
        new_y = player_y - 0.1 * math.sin(player_angle)
        if MAP[int(new_y)][int(new_x)] == 0:
            player_x, player_y = new_x, new_y
    if keys[pygame.K_LEFT]:
        new_x = player_x + 0.1 * math.sin(player_angle)
        new_y = player_y - 0.1 * math.cos(player_angle)
        if MAP[int(new_y)][int(new_x)] == 0:
            player_x, player_y = new_x, new_y
    if keys[pygame.K_RIGHT]:
        new_x = player_x - 0.1 * math.sin(player_angle)
        new_y = player_y + 0.1 * math.cos(player_angle)
        if MAP[int(new_y)][int(new_x)] == 0:
            player_x, player_y = new_x, new_y

    # Update player angle with mouse movement
    mouse_movement = pygame.mouse.get_rel()
    player_angle += mouse_movement[0] * mouse_sensitivity

    # Update bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.check_collision() or bullet.lifetime <= 0:
            bullets.remove(bullet)
    
    # Check for exit
    if int(player_x) == MAP_SIZE - 2 and int(player_y) == MAP_SIZE - 2:
        print("Congratulations! You've escaped the maze!")
        running = False
    
    draw_world()
    draw_gun()
    draw_minimap()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()