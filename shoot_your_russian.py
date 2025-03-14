import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Red Soviet Shooter")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)     # Terrorist
GREEN = (0, 255, 0)     # Civilian
BLUE  = (0, 0, 255)     # Crosshair
GRAY  = (100, 100, 100) # Building background

# Define a Window class to represent each window on the building
class Window:
    def __init__(self, rect):
        self.rect = rect
        self.state = 0       # 0 = empty, 1 = terrorist, 2 = civilian
        self.spawn_time = 0  # time when enemy appeared

# Create a grid of windows on the building (e.g., 3 rows x 4 columns)
rows = 3
cols = 4
window_width, window_height = 100, 100
margin_x = (WIDTH - cols * window_width) // (cols + 1)
margin_y = (HEIGHT - rows * window_height) // (rows + 1)

windows = []
for row in range(rows):
    for col in range(cols):
        x = margin_x + col * (window_width + margin_x)
        y = margin_y + row * (window_height + margin_y)
        rect = pygame.Rect(x, y, window_width, window_height)
        windows.append(Window(rect))

# Game parameters
score = 0
enemy_duration = 1500  # milliseconds enemy remains visible
spawn_interval = 1000  # spawn a new enemy every 1 second
last_spawn_time = pygame.time.get_ticks()

running = True
while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if any window was clicked
            for window in windows:
                if window.rect.collidepoint(mouse_pos) and window.state != 0:
                    # If terrorist, add point; if civilian, subtract point.
                    if window.state == 1:
                        score += 1
                    elif window.state == 2:
                        score -= 1
                    window.state = 0  # Clear the window

    # Spawn enemy in a random empty window every spawn_interval
    if current_time - last_spawn_time >= spawn_interval:
        last_spawn_time = current_time
        empty_windows = [w for w in windows if w.state == 0]
        if empty_windows:
            chosen = random.choice(empty_windows)
            # 70% chance for terrorist, 30% for civilian
            chosen.state = 1 if random.random() < 0.7 else 2
            chosen.spawn_time = current_time

    # Clear enemy if it stays too long
    for window in windows:
        if window.state != 0 and current_time - window.spawn_time > enemy_duration:
            window.state = 0

    # Drawing the game background and building
    screen.fill(GRAY)

    # Draw each window and, if applicable, its enemy
    for window in windows:
        pygame.draw.rect(screen, BLACK, window.rect, 2)  # Window frame
        if window.state == 1:  # Terrorist: red circle
            center = window.rect.center
            radius = min(window.rect.width, window.rect.height) // 4
            pygame.draw.circle(screen, RED, center, radius)
        elif window.state == 2:  # Civilian: green circle
            center = window.rect.center
            radius = min(window.rect.width, window.rect.height) // 4
            pygame.draw.circle(screen, GREEN, center, radius)

    # Draw a crosshair at the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.line(screen, BLUE, (mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), 2)
    pygame.draw.line(screen, BLUE, (mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), 2)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
