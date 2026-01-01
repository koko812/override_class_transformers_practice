import pygame as pg
import sys

pg.init()

screen = pg.display.set_mode((600, 500))
pg.display.set_caption("start this game!")

clock = pg.time.Clock()

running = True
frame_cnt = 0

while running:
    screen.fill((255,0,0))
    pg.display.flip() #これがないと赤くならない
    clock.tick(100)

    frame_cnt += 1
    if frame_cnt>100:
        running = False

print("display ended")