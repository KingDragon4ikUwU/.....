import pygame
from random import randrange as rnd
pygame.init()
WIDTH, HEIGHT = 1200, 800
fps = 60


scores = 0
pygame.display.set_caption('ARKANOID')
img = pygame.image.load('gamecontroller_23912.png')
pygame.display.set_icon(img)


pygame.mixer.music.load('fonk.mp3')
pygame.mixer.music.play(-1)
platform_w = 330
platform_h = 35
platform_speed = 25
platform = pygame.Rect(WIDTH // 2 - platform_w // 2, HEIGHT - platform_h - 10, platform_w, platform_h)



ball_radius = 20
ball_speed = 10
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]

color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# background image
img = pygame.image.load('poverhnost_fon_temnyy_pyatna_35126_1920x1080.jpg').convert()


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

#game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    # drawing

    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]

    pygame.draw.rect(sc, pygame.Color('dark red'), platform)
    pygame.draw.circle(sc, pygame.Color('navy'), ball.center, ball_radius)
    print('scores: ' + str(scores))

    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx

    if ball.centery < ball_radius:
        dy = -dy

    if ball.colliderect(platform) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, platform)

    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)

        scores += 1
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2
    if ball.bottom > HEIGHT:
        print('GAME OVER!')
        exit()
    elif not len(block_list):
        print('WIN!!!')
        exit()
    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and platform.left > 0:
        platform.left -= platform_speed
    if key[pygame.K_RIGHT] and platform.right < WIDTH:
        platform.right += platform_speed
    if key[pygame.K_a] and platform.left > 0:
        platform.left -= platform_speed
    if key[pygame.K_d] and platform.right < WIDTH:
       platform.right += platform_speed
    # update screen
    pygame.display.flip()
    clock.tick(fps)