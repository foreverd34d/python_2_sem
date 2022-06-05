import os
import pygame
import math

pygame.init()

SIZE = WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (30, 30, 46)
FPS = 60

GRAY = (49, 50, 68)
LIGHT_GRAY = (88, 91, 112)
YELLOW = (249, 226, 175)
PEACH = (250, 179, 135)

saturn_color = PEACH
io_color = YELLOW
evr_color = LIGHT_GRAY

pygame.display.set_caption("Jupiter")
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

center = (WIDTH / 2, HEIGHT / 2)

pygame.draw.circle(screen, saturn_color, center, 45)
pygame.draw.ellipse(screen, (144, 77, 48),
                    (center[0] + 7, center[1] + 10, 20, 7))

io_orb = 180
evr_orb = 270
x1, y1 = center[0] + 1, center[1] + io_orb
x2, y2 = center[0] + evr_orb, center[1]
io_r = 5
evr_r = 10
x3 = center[0] - 50
y3 = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.circle(screen, GRAY, center, 50)
    pygame.draw.circle(screen, saturn_color, center, 45)
    pygame.draw.ellipse(screen, (144, 77, 48),
                        (center[0] + 7, center[1] + 10, 20, 7))
    pygame.draw.circle(screen, (255, 255, 255), (x3, y3), 2)
    if y3 < HEIGHT + 1:
        x3 -= 0.00001 * x3**2
        y3 += 1
    if center[0] < x1 <= center[0] + io_orb:
        if y1 > center[1]:
            x1 += 1
            y1 = math.sqrt((io_orb**2) - (x1 - center[0])**2) + center[1]
            pygame.draw.circle(screen, io_color, (x1, y1), io_r)
        else:
            x1 -= 1
            y1 = -1 * math.sqrt((io_orb**2) - (x1 - center[0])**2) + center[1]
            pygame.draw.circle(screen, io_color, (x1, y1), io_r)
    else:
        if y1 < center[1]:
            x1 -= 1
            y1 = -1 * math.sqrt((io_orb**2) - (x1 - center[0])**2) + center[1]
            pygame.draw.circle(screen, io_color, (x1, y1), io_r)
        else:
            x1 += 1
            y1 = math.sqrt((io_orb**2) - (x1 - center[0])**2) + center[1]
            pygame.draw.circle(screen, io_color, (x1, y1), io_r)

    if center[0] < x2 <= center[0] + evr_orb:
        if y2 > center[1]:
            x2 += 1
            y2 = math.sqrt((evr_orb**2) - (x2 - center[0])**2) + center[1]
            pygame.draw.circle(screen, evr_color, (x2, y2), evr_r)
        else:
            x2 -= 1
            y2 = -1 * math.sqrt((evr_orb**2) - (x2 - center[0])**2) + center[1]

            pygame.draw.circle(screen, evr_color, (x2, y2), evr_r)
    else:
        if y2 < center[1]:
            x2 -= 1
            y2 = -1 * math.sqrt((evr_orb**2) - (x2 - center[0])**2) + center[1]
            pygame.draw.circle(screen, evr_color, (x2, y2), evr_r)
        else:
            x2 += 1
            y2 = math.sqrt((evr_orb**2) - (x2 - center[0])**2) + center[1]
            pygame.draw.circle(screen, evr_color, (x2, y2), evr_r)

    clock.tick(60)
    pygame.display.update()
