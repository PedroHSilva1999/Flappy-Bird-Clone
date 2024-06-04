import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

BIRD_WIDTH = 40
BIRD_HEIGHT = 30
PIPE_WIDTH = 60
PIPE_GAP = 200

gravity = 0.5
bird_movement = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

bird_image = pygame.image.load('bird.png')
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
pipe_image.fill(GREEN)

font = pygame.font.Font(None, 36)

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_image, (pipe['x'], pipe['y']))
        screen.blit(pipe_image, (pipe['x'], pipe['y'] - PIPE_GAP - SCREEN_HEIGHT))

def show_game_over_screen(score):
    game_over_font = pygame.font.Font(None, 74)
    restart_font = pygame.font.Font(None, 36)
    
    game_over_text = game_over_font.render("Game Over", True, BLACK)
    restart_text = restart_font.render("Pressione qualquer tecla para reiniciar", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)

    screen.fill(WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    global bird_movement

    while True:
        bird_x = 50
        bird_y = SCREEN_HEIGHT // 2

        pipes = []
        pipe_frequency = 1500 
        last_pipe = pygame.time.get_ticks() - pipe_frequency

        clock = pygame.time.Clock()
        running = True
        score = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_movement = -10

            bird_movement += gravity
            bird_y += bird_movement

            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(150, SCREEN_HEIGHT - 150)
                pipes.append({'x': SCREEN_WIDTH, 'y': pipe_height})
                last_pipe = time_now

            for pipe in pipes:
                pipe['x'] -= 5

            pipes = [pipe for pipe in pipes if pipe['x'] > -PIPE_WIDTH]

            for pipe in pipes:
                if (bird_x + BIRD_WIDTH > pipe['x'] and bird_x < pipe['x'] + PIPE_WIDTH):
                    if (bird_y < pipe['y'] - PIPE_GAP or bird_y + BIRD_HEIGHT > pipe['y']):
                        running = False

            if bird_y > SCREEN_HEIGHT - BIRD_HEIGHT or bird_y < 0:
                running = False

            for pipe in pipes:
                if pipe['x'] == bird_x:
                    score += 1

            screen.fill(WHITE)
            screen.blit(bird_image, (bird_x, bird_y))
            draw_pipes(pipes)

            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()

            clock.tick(30)

        show_game_over_screen(score)

if __name__ == "__main__":
    main()
