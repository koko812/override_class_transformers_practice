import pygame as pg
import sys

pg.init() #これはやらなくてもなぜか動いた（なんで）

screen = pg.display.set_mode((600, 500)) #これは初期化しないとそもそも fill できないので必要
pg.display.set_caption("start this game!")

clock = pg.time.Clock()

running = True
frame_cnt = 0

while running:
    screen.fill((255,0,0))
    pg.display.flip() #これがないと赤くならない
    clock.tick(50)

    frame_cnt += 1
    if frame_cnt>100:
        running = False

print("display ended")