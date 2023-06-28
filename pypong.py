import pygame
import random

pygame.font.init()

WIDTH, HEIGHT = 800, 600

FONT = pygame.font.Font("Pixeled.ttf", 20)
FONT_COLOR = (255,255,255)

BG_COLOR = (0,0,0)
PADDLE_COLOR = (255,255,255)

PADDLE_LEFT_POS = (10, HEIGHT/2 - 50)
PADDLE_LEFT = pygame.Rect(*PADDLE_LEFT_POS, 10, 100)

PADDLE_RIGHT_POS = (WIDTH - 20, HEIGHT/2 - 50)
PADDLE_RIGHT = pygame.Rect(*PADDLE_RIGHT_POS, 10, 100)

PADDLE_SPD = 8

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPong")

FPS = 60

class Ball:
    def __init__(self, color, radius, speed):
        self.color = color
        self.radius = radius
        self.speed = speed

        self.x_vel = 0
        self.y_vel = 0

    def set_vel(self):
        self.x_vel = random.choice((-1, 1)) * self.speed
        self.y_vel = random.choice((-1, 1)) * self.speed

    def move(self, rect):
        rect.x -= self.x_vel
        rect.y -= self.y_vel

    def bounce_y(self):
        self.y_vel = -self.y_vel
    def bounce_x(self):
        self.x_vel = -self.x_vel

BALL_SPD = 5
BALL_COLOR = (255,255,255)
BALL_RADIUS = 15

BALL = Ball(BALL_COLOR, BALL_RADIUS, BALL_SPD)

BALL_POS = (WIDTH/2 - BALL.radius, HEIGHT/2 - BALL.radius)

def draw(paddle_left, paddle_right, ball, left_score, right_score):
    WIN.fill(BG_COLOR)

    pygame.draw.rect(WIN, PADDLE_COLOR, paddle_left)
    pygame.draw.rect(WIN, PADDLE_COLOR, paddle_right)

    pygame.draw.circle(WIN, BALL.color, (ball.centerx, ball.centery), BALL.radius)
    # Big Note: a circle's position does not start in the topleft, it starts at the center

    score = FONT.render(str(left_score)+"-"+str(right_score), False, FONT_COLOR)
    WIN.blit(score, (WIDTH/2 - score.get_width()/2, 0))

    pygame.display.update()

def handle_movement(paddle_left, paddle_right, keys):
    if keys[pygame.K_w] and paddle_left.y > 0:
        paddle_left.y -= PADDLE_SPD
    if keys[pygame.K_s] and paddle_left.y + paddle_left.height < HEIGHT:
        paddle_left.y += PADDLE_SPD
    if keys[pygame.K_UP] and paddle_right.y > 0:
        paddle_right.y -= PADDLE_SPD
    if keys[pygame.K_DOWN] and paddle_right.y + paddle_right.height < HEIGHT:
        paddle_right.y += PADDLE_SPD

def next_round(paddle_left, paddle_right, ball, ball_rect):
    paddle_left.x = PADDLE_LEFT_POS[0]
    paddle_left.y = PADDLE_LEFT_POS[1]

    paddle_right.x = PADDLE_RIGHT_POS[0]
    paddle_right.y = PADDLE_RIGHT_POS[1]

    ball_rect.x = BALL_POS[0]
    ball_rect.y = BALL_POS[1]
    ball.set_vel()

def main():
    clock = pygame.time.Clock()

    ball = pygame.Rect(*BALL_POS, BALL.radius*2, BALL.radius*2)
    BALL.set_vel()

    right_score = 0
    left_score = 0

    run = True
    while run:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

        BALL.move(ball)
        if ball.y <= 0 or ball.y + ball.height > HEIGHT:
            BALL.bounce_y()
        if ball.colliderect(PADDLE_LEFT) or ball.colliderect(PADDLE_RIGHT):
            BALL.bounce_x()
        if ball.x <= 0:
            next_round(PADDLE_LEFT, PADDLE_RIGHT, BALL, ball)
            right_score += 1
        if ball.x + ball.width > WIDTH:
            next_round(PADDLE_LEFT, PADDLE_RIGHT, BALL, ball)
            left_score += 1

        keys = pygame.key.get_pressed()
        handle_movement(PADDLE_LEFT, PADDLE_RIGHT, keys)

        draw(PADDLE_LEFT, PADDLE_RIGHT, ball, left_score, right_score)

    pygame.quit()

main()

# code by - ME