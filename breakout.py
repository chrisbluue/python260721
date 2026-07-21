import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_COLOR = (0, 180, 255)
BALL_COLOR = (255, 255, 0)
BRICK_COLORS = [(255, 80, 80), (255, 180, 80), (80, 200, 80), (80, 120, 255)]

paddle_w, paddle_h = 100, 20
paddle_x = (WIDTH - paddle_w) // 2
paddle_y = HEIGHT - 40
paddle_speed = 8

ball_radius = 8
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 4
ball_speed_y = -4
ball_active = False

brick_w, brick_h = 50, 20
brick_gap = 10
brick_rows, brick_cols = 5, 8
bricks = []

score = 0
lives = 3
game_over = False
win = False

font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)


def create_bricks():
    bricks.clear()
    for row in range(brick_rows):
        for col in range(brick_cols):
            x = 20 + col * (brick_w + brick_gap)
            y = 60 + row * (brick_h + brick_gap)
            bricks.append([pygame.Rect(x, y, brick_w, brick_h), BRICK_COLORS[row % len(BRICK_COLORS)]])


def reset_game():
    global paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, ball_active
    global score, lives, game_over, win

    paddle_x = (WIDTH - paddle_w) // 2
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = random.choice([-4, 4])
    ball_speed_y = -4
    ball_active = False

    score = 0
    lives = 3
    game_over = False
    win = False
    create_bricks()


def launch_ball():
    global ball_active
    ball_active = True


reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not win and not ball_active:
                launch_ball()
            elif event.key == pygame.K_RETURN and (game_over or win):
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over and not win:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            paddle_x += paddle_speed

        paddle_x = max(0, min(WIDTH - paddle_w, paddle_x))

        if ball_active:
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
                ball_speed_x *= -1
                ball_x = max(ball_radius, min(WIDTH - ball_radius, ball_x))

            if ball_y - ball_radius <= 0:
                ball_speed_y *= -1
                ball_y = ball_radius

            paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_w, paddle_h)
            ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)

            if paddle_rect.colliderect(ball_rect) and ball_speed_y > 0:
                ball_y = paddle_y - ball_radius
                ball_speed_y = -abs(ball_speed_y)
                offset = (ball_x - (paddle_x + paddle_w / 2)) / (paddle_w / 2)
                ball_speed_x = offset * 6

            if ball_y + ball_radius >= HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    ball_x = WIDTH // 2
                    ball_y = HEIGHT // 2
                    ball_speed_x = random.choice([-4, 4])
                    ball_speed_y = -4
                    ball_active = False

            for brick in bricks[:]:
                rect, color = brick
                if rect.colliderect(ball_rect):
                    bricks.remove(brick)
                    score += 100

                    if ball_rect.centerx < rect.left or ball_rect.centerx > rect.right:
                        ball_speed_x *= -1
                    else:
                        ball_speed_y *= -1
                    break

            if not bricks:
                win = True

    screen.fill(BLACK)

    for rect, color in bricks:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, WHITE, rect, 1)

    pygame.draw.rect(screen, PADDLE_COLOR, (paddle_x, paddle_y, paddle_w, paddle_h))
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), ball_radius)

    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))

    if game_over:
        over_text = big_font.render("GAME OVER", True, WHITE)
        restart_text = font.render("Press Enter to Restart", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
    elif win:
        win_text = big_font.render("YOU WIN!", True, WHITE)
        restart_text = font.render("Press Enter to Restart", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
    else:
        start_text = font.render("Press Space to Start", True, WHITE)
        if not ball_active:
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()