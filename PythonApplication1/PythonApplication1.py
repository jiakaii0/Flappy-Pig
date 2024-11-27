import pygame
import random

pygame.init()


# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Pig")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Game Variables
gravity = 0.5
bird_y_velocity = 0
bird_x = 100
bird_y = 300
bird_width = 30
bird_height = 30

pipe_width = 50
pipe_gap = 175
pipe_velocity = 15

score = 0
running = True

# Load bird image
bird_image = pygame.image.load("pig.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))

# Clock for controlling frame rate
clock = pygame.time.Clock()


def try_again_screen(score):
    """Displays the Try Again screen."""
    while True:
        screen.fill(BLUE)
        
        # Display Game Over text
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        
        # Display Score
        font = pygame.font.Font(None, 48)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
        
        # Display Try Again Option
        try_again_text = font.render("Press R to Try Again", True, WHITE)
        screen.blit(try_again_text, (SCREEN_WIDTH // 2 - try_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        
        # Display Quit Option
        quit_text = font.render("Press Q to Quit", True, WHITE)
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 90))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    exit()


def reset_game():
    """Resets the game variables."""
    global bird_y, bird_y_velocity, pipe_x, pipe_y, score
    bird_y = 300
    bird_y_velocity = 0
    pipe_x = SCREEN_WIDTH
    pipe_y = random.randint(200, SCREEN_HEIGHT - pipe_gap - 50)
    score = 0


# Initialize pipes
pipe_x = SCREEN_WIDTH
pipe_y = random.randint(200, SCREEN_HEIGHT - pipe_gap - 50)

# Main game loop
while running:
    clock.tick(144)  # Increase to 60 frames per second

    screen.fill(BLUE)  # Background color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_velocity = -10

    # Apply gravity
    bird_y_velocity += gravity
    bird_y += bird_y_velocity

    # Draw the bird
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)  # Create bird's rectangle for collision
    screen.blit(bird_image, (bird_x, bird_y))

    # Move and draw pipes
    pipe_x -= pipe_velocity
    if pipe_x < -pipe_width:
        pipe_x = SCREEN_WIDTH
        pipe_y = random.randint(200, SCREEN_HEIGHT - pipe_gap - 50)
        score += 1

    top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_y)
    bottom_pipe = pygame.Rect(pipe_x, pipe_y + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe_y - pipe_gap)
    pygame.draw.rect(screen, GREEN, top_pipe)
    pygame.draw.rect(screen, GREEN, bottom_pipe)

    # Collision detection
    if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe) or bird_y < 0 or bird_y > SCREEN_HEIGHT:
        try_again_screen(score)
        reset_game()

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
