import pygame
import random
from pygame.locals import RLEACCEL, K_UP, K_DOWN, K_ESCAPE, K_SPACE, KEYDOWN, QUIT

# Initialize pygame and the mixer for sound
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Side-Scrolling Game")

# Load the background music and sound effects
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.set_volume(0.3)

move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")
shoot_sound = pygame.mixer.Sound("Shoot.ogg")
collectible_sound = pygame.mixer.Sound("Collectible.wav")

move_up_sound.set_volume(0.3)
move_down_sound.set_volume(0.6)
collision_sound.set_volume(0.4)
shoot_sound.set_volume(0.3)
collectible_sound.set_volume(0.3)

# Background color
BACKGROUND_COLOR = (135, 206, 250)

# Function to display text on the screen
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Player class with sprite image
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.health = 100
        self.lives = 3
        self.score = 0
        self.speed = 3

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
            move_up_sound.play()

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        projectile = Projectile(self.rect.right, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)
        move_down_sound.play()

# Projectile class for shooting
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((10, 5))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(x, y))
        self.speed_x = 6

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Enemy class with sprite image
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.level = level
        size = 40 if level == 1 else 60 if level == 2 else 120
        self.surf = pygame.Surface((size, size))
        self.surf.fill((255, 0, 0) if level < 3 else (255, 255, 0))  # Red for normal, yellow for boss
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 2 if level < 3 else 1  # Slower for the boss in Level 3

        # Set enemy health based on the level
        self.health = 1 if level == 1 else 2 if level == 2 else 3  # 2 shots for Level 2, 3 for boss

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()  # Remove enemy if it exits the screen

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Kill only when health reaches 0

# Cloud class for background visuals
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-3, 0)
        if self.rect.right < 0:
            self.kill()

# Collectible class for health and life boosts
class Collectible(pygame.sprite.Sprite):
    def __init__(self, collectible_type):
        super().__init__()
        self.collectible_type = collectible_type
        if self.collectible_type == 'health':
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((255, 165, 0))
        elif self.collectible_type == 'life':
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((0, 0, 255))
        
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 2

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Adjust entity position relative to the camera
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Update camera position to follow the target (player)
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2

        # Limit scrolling to the bounds of the game world
        x = min(0, x)  # Prevent scrolling past the left boundary
        y = min(0, y)  # Prevent scrolling past the top boundary
        x = max(-(self.width - SCREEN_WIDTH), x)  # Prevent scrolling past the right boundary
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Prevent scrolling past the bottom boundary

        # Update camera rect with new position
        self.camera = pygame.Rect(x, y, self.width, self.height)

# In the main game loop, you'd use this Camera class to adjust the positions of all entities:
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

# Function to show level screens
def level_start(level):
    pygame.mixer.music.pause()
    screen.fill((0, 0, 0))
    draw_text(screen, f"Level {level}", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(600)

# Function to show level complete screen
def level_complete(level):
    pygame.mixer.music.pause()
    screen.fill((0, 0, 0))
    draw_text(screen, f"Level {level} Complete!", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, "Press Q to Quit", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_key(auto_proceed=True)

# Game over screen
def game_over():
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, "Press R to Restart or Q to Quit", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_key(game_over=True)

# You Win screen
def you_win():
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    draw_text(screen, "YOU WIN!", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, "Press R to Restart or Q to Quit", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_key(game_over=True)

# Wait for key press or automatically proceed after delay
def wait_for_key(game_over=False, auto_proceed=False):
    pygame.event.clear()
    waiting = True
    start_time = pygame.time.get_ticks()

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_r and game_over:
                    game_loop()

        if auto_proceed and pygame.time.get_ticks() - start_time > 2000:
            waiting = False

# Set up sprite groups
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create timers for enemy and cloud spawn
ADDENEMY = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2
ADDCOLLECTIBLE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDENEMY, 1500)
pygame.time.set_timer(ADDCLOUD, 2000)
pygame.time.set_timer(ADDCOLLECTIBLE, 5000)

# Main game loop
def game_loop():
    global player, all_sprites, enemies, projectiles, collectibles, clouds
    level = 1
    player = Player()
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    clock = pygame.time.Clock()
    enemies_killed = 0
    collectible_count = 0
    boss_spawned = False
    
    # Update camera to follow the player
    camera.update(player)

    # When rendering, apply the camera transformation to each entity
    for entity in all_sprites:
        screen.blit(entity.surf, camera.apply(entity))

    def start_new_level(new_level):
        nonlocal enemies_killed, collectible_count, boss_spawned
        enemies_killed = 0
        collectible_count = 0
        
        # Clear enemies, collectibles, projectiles, and clouds before starting the new level
        enemies.empty()
        collectibles.empty()  # Clear all collectibles
        projectiles.empty()
        clouds.empty()
        
        boss_spawned = False
        all_sprites.update()
        all_sprites.add(player)
        level_start(new_level)
        pygame.mixer.music.unpause()

    start_new_level(level)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    player.shoot()
            elif event.type == QUIT:
                running = False
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            elif event.type == ADDCOLLECTIBLE:
                if collectible_count < 2 and level < 3:
                    if enemies_killed >= collectible_count + 1:
                        collectible_type = 'health' if collectible_count == 0 else 'life'
                        new_collectible = Collectible(collectible_type)
                        collectibles.add(new_collectible)
                        all_sprites.add(new_collectible)
                        collectible_count += 1
                else:
                    collectible_count = 0  # Reset collectible count for new levels

        # Spawn enemies based on level
        if level < 3:
            if len(enemies) < 1:
                enemy = Enemy(level)
                all_sprites.add(enemy)
                enemies.add(enemy)

        else:  # Boss level
            if boss_spawned and len(enemies) == 0:  # If boss is not present anymore (killed or passed)
                boss_spawned = False  # Reset the boss_spawned flag so it can respawn

            if not boss_spawned:  # If the boss is not present, spawn it again
                boss = Enemy(level)  # Create the boss enemy
                all_sprites.add(boss)
                enemies.add(boss)
                boss_spawned = True

        # Update all entities
        all_sprites.update()

        # Check for collisions between projectiles and enemies
        for enemy in enemies:
            if pygame.sprite.spritecollide(enemy, projectiles, True):
                enemy.take_damage(1)  # Reduce enemy health by 1 for each hit
                if enemy.health <= 0:  # Enemy killed
                    enemies_killed += 1
                    player.score += 10 if level == 1 else 20 if level == 2 else 30

        # Check for collisions between player and enemies
        for enemy in pygame.sprite.spritecollide(player, enemies, False):
            collision_sound.play()
            damage = 20 if level == 1 else 30 if level == 2 else 40
            player.health -= damage
            boss_spawned = False
            enemy.kill()

            if player.health <= 0:
                player.lives -= 1
                player.health = 100
                if player.lives <= 0:
                    game_over()
                    running = False

        # Check for collisions between player and collectibles
        collected = pygame.sprite.spritecollide(player, collectibles, True)
        for collect in collected:
            collectible_sound.play()
            if collect.collectible_type == 'health':
                player.health = min(player.health + 20, 100)
            elif collect.collectible_type == 'life':
                player.lives += 1
            collect.kill()

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Display health, lives, and score
        draw_text(screen, f"Health: {player.health}", 22, 80, 10)
        draw_text(screen, f"Lives: {player.lives}", 22, 200, 10)
        draw_text(screen, f"Score: {player.score}", 22, SCREEN_WIDTH // 2, 10)

        pygame.display.flip()

        # Level completion logic
        if level == 1 and enemies_killed >= 5:
            pygame.time.wait(500)
            # Clear collectibles when the level ends
            for collectible in collectibles:
                collectible.kill()
            level_complete(level)
            level += 1
            start_new_level(level)
        elif level == 2 and enemies_killed >= 3:
            pygame.time.wait(500)
            for collectible in collectibles:
                collectible.kill()

            level_complete(level)
            level += 1
            start_new_level(level)
        elif level == 3 and enemies_killed >= 1:  # Boss defeated
            pygame.time.wait(500)
            for collectible in collectibles:
                collectible.kill()
            you_win()
            running = False

    pygame.quit()

game_loop()
