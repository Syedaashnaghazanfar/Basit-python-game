import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)
PIPE_GREEN = (34, 139, 34)
BIRD_YELLOW = (255, 223, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER = (0, 180, 255)

# Screen dimensions
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Fonts
pygame.display.set_caption("Flappy Bird - By Abdulbasit Ali")
font = pygame.font.Font(None, 36)

# Bird settings
bird_size = 30
bird_x = WIDTH // 6
bird_y = HEIGHT // 2
bird_dy = 0
gravity = 0.5
jump_strength = -5

# Pipe settings
pipe_width = 80
pipe_gap = 150
pipe_x = WIDTH
pipe_height = random.randint(150, 400)
initial_pipe_speed = 3
pipe_speed = initial_pipe_speed  # This will increase as score rises

# Game settings
score = 0
clock = pygame.time.Clock()
running = True
game_started = False
game_over = False

# Background gradient
def draw_background():
    for y in range(HEIGHT):
        color = (
            int(LIGHT_BLUE[0] + (DARK_BLUE[0] - LIGHT_BLUE[0]) * (y / HEIGHT)),
            int(LIGHT_BLUE[1] + (DARK_BLUE[1] - LIGHT_BLUE[1]) * (y / HEIGHT)),
            int(LIGHT_BLUE[2] + (DARK_BLUE[2] - LIGHT_BLUE[2]) * (y / HEIGHT)),
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

# Function to display "Click to Play" text
def display_start_text():
    start_text = font.render("Click to Play", True, WHITE)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))

# Function to display "Game Over" screen
def display_game_over():
    game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))

    # Draw Restart and Exit buttons
    restart_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 20, 120, 40)
    exit_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 80, 120, 40)
    
    pygame.draw.rect(screen, BUTTON_COLOR, restart_button)
    pygame.draw.rect(screen, BUTTON_COLOR, exit_button)

    # Button text
    restart_text = font.render("Restart", True, WHITE)
    exit_text = font.render("Exit", True, WHITE)
    
    screen.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2, restart_button.y + 5))
    screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, exit_button.y + 5))

    return restart_button, exit_button

# Game loop
while running:
    draw_background()

    if game_started and not game_over:
        # Gradually increase pipe speed based on the score
        pipe_speed = initial_pipe_speed + (score // 5)  # Increase speed every 5 points

        # Draw bird
        bird_rect = pygame.Rect(bird_x - bird_size // 2, bird_y - bird_size // 2, bird_size, bird_size)
        pygame.draw.ellipse(screen, BIRD_YELLOW, bird_rect)

        # Move bird
        bird_dy += gravity
        bird_y += int(bird_dy)

        # Draw pipes
        pipe_rect_top = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        pipe_rect_bottom = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT - (pipe_height + pipe_gap))
        pygame.draw.rect(screen, PIPE_GREEN, pipe_rect_top)
        pygame.draw.rect(screen, PIPE_GREEN, pipe_rect_bottom)

        # Move pipes
        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(150, 400)
            score += 1

        # Check collisions
        if bird_y > HEIGHT or bird_y < 0 or bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
            game_over = True

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    elif game_over:
        # Display game over screen with restart and exit options
        restart_button, exit_button = display_game_over()

    else:
        # Display "Click to Play" if game hasn't started
        display_start_text()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                # Start game on click
                game_started = True
            elif game_over:
                # Check if restart or exit button was clicked
                if restart_button.collidepoint(event.pos):
                    # Restart the game
                    bird_y = HEIGHT // 2
                    bird_dy = 0
                    pipe_x = WIDTH
                    score = 0
                    pipe_speed = initial_pipe_speed  # Reset speed
                    game_over = False
                    game_started = True
                elif exit_button.collidepoint(event.pos):
                    # Exit the game
                    pygame.quit()
                    sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_started and not game_over:
            # Flap the bird up when space is pressed
            bird_dy = jump_strength

    pygame.display.flip()
    clock.tick(30)  # FPS

pygame.quit()
