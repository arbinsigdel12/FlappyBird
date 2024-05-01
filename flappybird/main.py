import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Tower Defense")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define the player
player_img = pygame.Surface((30, 30))
player_img.fill(RED)
player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT-50))

# Define the enemy
enemy_img = pygame.Surface((30, 30))
enemy_img.fill(WHITE)
enemies = []

# Define the tower
tower_img = pygame.Surface((50, 50))
tower_img.fill((0, 255, 0))
towers = []

# Game variables
clock = pygame.time.Clock()
spawn_timer = -20
spawn_delay = 1000  # milliseconds
enemy_speed = 10
score = 0

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Place tower when mouse is clicked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                pos = pygame.mouse.get_pos()
                tower_rect = tower_img.get_rect(center=pos)
                towers.append(tower_rect)

    # Enemy spawning
    spawn_timer += clock.get_rawtime()
    if spawn_timer >= spawn_delay:
        spawn_timer = 0
        enemy_rect = enemy_img.get_rect(center=(random.randint(50, WIDTH-50), 0))
        enemies.append(enemy_rect)

    # Move enemies
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            score -= 1

    # Check for collisions between towers and enemies
    for tower in towers:
        for enemy in enemies:
            if tower.colliderect(enemy):
                enemies.remove(enemy)
                score += 1

    # Draw everything
    screen.blit(player_img, player_rect)
    for tower in towers:
        screen.blit(tower_img, tower)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
