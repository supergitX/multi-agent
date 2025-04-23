import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Floppy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 128, 0)

# Bird properties
BIRD_X = 50
BIRD_Y = SCREEN_HEIGHT // 2
BIRD_RADIUS = 16
BIRD_GRAVITY = 0.5
BIRD_JUMP_HEIGHT = -10
bird_velocity = 0

# Pipe properties
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_VELOCITY = -3
pipes = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game state
game_over = False

# Clock
clock = pygame.time.Clock()