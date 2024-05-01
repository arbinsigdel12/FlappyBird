import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 400 
SCREEN_HEIGHT = 512
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_GAP = 100
GRAVITY = 0.25
FLAP_SPEED = -5
FPS = 60
FONT_SIZE = 30
FONT_COLOR = (255, 255, 255)

# Colors
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load assets
bg_surface = pygame.image.load('assets/background.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
bird_surface = pygame.image.load('assets/bird1.png').convert_alpha()
bird_surface = pygame.transform.scale(bird_surface, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_surface = pygame.image.load('assets/pipe.jpg').convert_alpha()
pipe_surface = pygame.transform.scale(pipe_surface, (PIPE_WIDTH, PIPE_HEIGHT))

# Fonts
font = pygame.font.SysFont(None, FONT_SIZE)

# Function to create a new pipe
def create_pipe():
    random_pipe_pos = random.randint(100, SCREEN_HEIGHT - 200)
    bottom_pipe = pipe_surface.get_rect(midtop=(SCREEN_WIDTH + 20, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(SCREEN_WIDTH + 20, random_pipe_pos - PIPE_GAP))
    return bottom_pipe, top_pipe

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Function to check for collisions
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= SCREEN_HEIGHT - 50:
        return False

    return True

# Function to rotate the bird
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

# Function to show the score
def display_score():
    score_surface = font.render(f'Score: {int(score)}', True, FONT_COLOR)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 50))
    screen.blit(score_surface, score_rect)

# Game variables
bird_rect = bird_surface.get_rect(center=(50, SCREEN_HEIGHT / 2))
bird_movement = 0
gravity = GRAVITY
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
score = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = FLAP_SPEED
        if event.type == SPAWNPIPE:
            pipes.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))

    # Bird
    bird_movement += gravity
    rotated_bird = rotate_bird(bird_surface)
    bird_rect.centery += bird_movement
    screen.blit(rotated_bird, bird_rect)

    # Pipes
    pipes = move_pipes(pipes)
    draw_pipes(pipes)

    # Collision
    if not check_collision(pipes):
        break

    # Score
    for pipe in pipes:
        if pipe.centerx == 50:
            score += 0.5

    display_score()

    pygame.display.update()
    pygame.time.Clock().tick(FPS)
