import pygame as pg

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pg.init() #実はなくても動くっぽい，不具合はわからんが
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pg.time.Clock()

runnning=True
while runnning:
    screen.fill((0,0,255))
    pg.display.flip()
    pg.time.delay(1000)
    runnning=False
    break

print("end")