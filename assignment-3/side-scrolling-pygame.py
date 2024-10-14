import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60


# Load assets
PLAYER_IMAGE = pygame.Surface((50, 30))  # Temporary tank shape
PLAYER_IMAGE.fill(GREEN)


COLLECTIBLE_IMAGE = pygame.Surface((20, 20))
COLLECTIBLE_IMAGE.fill((0, 0, 255))

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect(midbottom=(100, SCREEN_HEIGHT - 50))
        self.speed = 5
        self.jump_power = -15
        self.gravity = 1
        self.velocity_y = 0  # Vertical speed for jumping
        self.health = 100
        self.lives = 3
        self.is_jumping = False
        self.score = 0

    def move(self, direction):
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed

    def jump(self):
        if not self.is_jumping:  # Allow jumping only if the player is not in the air
            self.is_jumping = True
            self.velocity_y = self.jump_power  # Apply upward force for jumping

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = COLLECTIBLE_IMAGE
        self.rect = self.image.get_rect(center=(x, y))
        self.type = type

    def collect(self, player):
        if self.type == "health":
            player.health += 20
        elif self.type == "life":
            player.lives += 1
        self.kill()

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.level = 1
        self.score = 0
        self.enemies_defeated = 0
        self.boss_defeated = False
        self.game_over = False