import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
FPS = 60

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Side-Scrolling Game")

# Functions for displaying text on the screen
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)  # Default Pygame font
    text_surface = font.render(text, True, WHITE)  # Render the text
    text_rect = text_surface.get_rect()  # Get the text rectangle
    text_rect.midtop = (x, y)  # Position the text in the middle
    surface.blit(text_surface, text_rect)  # Draw the text on the given surface

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.speed_y = 0
        self.health = 100
        self.lives = 3
        self.score = 0

    def update(self):
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed_y = -5
        elif keys[pygame.K_DOWN]:
            self.speed_y = 5
        else:
            self.speed_y = 0

        self.rect.y += self.speed_y

        # Keep the player on the screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        projectile = Projectile(self.rect.right, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.lives -= 1
            self.health = 100
            if self.lives <= 0:
                game_over()

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 10

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        size = 40 if level == 1 else 60 if level == 2 else 80  # Enemies are bigger in each level
        self.image = pygame.Surface((size, size))
        self.image.fill(RED if level < 3 else YELLOW)  # Boss is yellow in level 3
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed_x = random.randint(3, 6) if level < 3 else 2  # Boss is slower
        self.health = 20 if level == 1 else 40 if level == 2 else 100  # Boss has more health

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()
            # Score for the player if the enemy passes
            player.score += 5

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            player.score += 10  # Increase score
            global enemies_killed
            enemies_killed += 1  # Track enemies killed

# Game over screen
def game_over():
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    draw_text(screen, "Press R to Restart or Q to Quit", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_key(game_over=True)

# You Win screen
def you_win():
    screen.fill(BLACK)
    draw_text(screen, "YOU WIN!", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    draw_text(screen, "Press R to Restart or Q to Quit", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_key(game_over=True)

# Level complete screen
def level_complete(level):
    pygame.event.clear()  # Clear event queue to prevent extra keypresses
    screen.fill(BLACK)
    draw_text(screen, f"Level {level} Complete!", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    draw_text(screen, "Press N to go to next level or Q to Quit", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_key(level_complete=True)

# Level start screen (with 20ms wait)
def level_start(level):
    screen.fill(BLACK)
    draw_text(screen, f"Level {level}", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(600)  # Automatically move to the game after 700 ms

# Wait for key press
def wait_for_key(game_over=False, level_complete=False):
    pygame.event.clear()  # Clear any lingering events before waiting
    waiting = True
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
                    game_loop()  # Restart game loop on 'R'
                if event.key == pygame.K_n and level_complete:
                    waiting = False  # Move to the next level after pressing N

# Main game loop
def game_loop():
    global player, all_sprites, projectiles, enemies, level, enemy_count, enemies_killed
    level = 1
    player = Player()
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    all_sprites.add(player)
    enemies_killed = 0
    enemy_count = 0

    running = True
    clock = pygame.time.Clock()

    def start_new_level(new_level):
        global enemies_killed, enemy_count
        enemies_killed = 0
        enemy_count = 0
        all_sprites.empty()
        projectiles.empty()
        enemies.empty()
        all_sprites.add(player)

        level_start(new_level)

    start_new_level(level)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update game objects
        all_sprites.update()

        # Spawn enemies based on level
        if level < 3:  # Normal enemies for level 1 and 2
            if len(enemies) < 1:  # Only allow one enemy at a time
                enemy = Enemy(level)
                all_sprites.add(enemy)
                enemies.add(enemy)
                enemy_count += 1

        else:  # Level 3 - Boss level
            if len(enemies) == 0 and enemies_killed == 0:  # Only spawn the boss once
                boss = Enemy(level)
                all_sprites.add(boss)
                enemies.add(boss)

        # Check for collisions between projectiles and enemies
        hits = pygame.sprite.groupcollide(enemies, projectiles, False, True)
        for hit in hits:
            hit.take_damage(10)

        # Check for collisions between player and enemies
        hits = pygame.sprite.spritecollide(player, enemies, False)
        for hit in hits:
            # Health reduction based on level
            damage = 30 if level == 1 else 50 if level == 2 else 80
            player.take_damage(damage)
            hit.kill()  # Enemy disappears on collision
            enemy_count -= 1

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {player.score}", 22, SCREEN_WIDTH // 2, 10)
        draw_text(screen, f"Health: {player.health}", 22, 80, 10)
        draw_text(screen, f"Lives: {player.lives}", 22, 200, 10)

        pygame.display.flip()  # Ensure screen updates

        # Level completion logic with a brief delay after the last enemy is killed
        if level == 1 and enemies_killed >= 4:
            pygame.time.wait(500)  # Short delay to show the last enemy being killed
            level_complete(level)
            waiting_for_next_level = True
            while waiting_for_next_level:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_n:
                            level += 1
                            start_new_level(level)
                            waiting_for_next_level = False
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            exit()

        elif level == 2 and enemies_killed >= 2:
            pygame.time.wait(500)  # Short delay to show the last enemy being killed
            level_complete(level)
            waiting_for_next_level = True
            while waiting_for_next_level:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_n:
                            level += 1
                            start_new_level(level)
                            waiting_for_next_level = False
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            exit()

        elif level == 3 and enemies_killed >= 1:  # Boss defeated
            pygame.time.wait(500)  # Short delay to show the boss being killed
            you_win()
            return

    pygame.quit()

# Run the game loop
level_start(1)  # Show the first level screen
game_loop()
