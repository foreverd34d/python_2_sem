import pygame as pg
from pygame.locals import *
import sys


class Oval(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((60, 60))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, BLACK, (WIDTH // 2, HEIGHT // 2), 4)
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        self.rect.x += 1
        self.rect.y -= 1

pg.init()

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
WIDTH = 600
HEIGHT = 400

scr = pg.display.set_mode((600, 400))
scr.fill(WHITE)
clock = pg.time.Clock()

all = pg.sprite.Group()

oval = Oval()
all.add(oval)

run = True
while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == QUIT:
            run = False

    all.update()

    scr.fill(WHITE)
    all.draw(scr)
    pg.display.flip()

pg.quit()
