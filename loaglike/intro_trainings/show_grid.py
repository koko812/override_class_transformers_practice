import pygame as pg
import sys
import math

pg.init() 

screen = pg.display.set_mode((600, 500))
pg.display.set_caption("start this game!")

clock = pg.time.Clock()
running = True
frame_cnt = 0

pg.font.init()
font = pg.font.Font(None, 50)
chars = {chr(ord('a')+i):font.render(chr(ord('A')+i), 0, (255,0,0)) for i in range(ord('z')-ord('a')+1)}

game_crear_font = pg.font.Font(None, 50)
game_crear_surface = game_crear_font.render("game_clear", 0, (255,0,0))


cx = 100
cy = 100

grid = [0] * 9
grid[4] = 1
grid[5] = -1
grid_size = 300
grid_top = 100
grid_left = 100
grid_line_width = 3

panes = []
pane_size = grid_size//3

clear_flag = False

maru_font = pg.font.Font(None, int(pane_size*1.5))
maru_surface = maru_font.render("o",1,(255,255,255))
batu_font = pg.font.Font(None, int(pane_size*1.5))
batu_surface = maru_font.render("×",1,(255,255,255))

screen_w, screen_h = screen.get_size()

while running:
    screen.fill((0,0,0))
    pg.draw.circle(screen, (255,0,0), (cx, cy), 20)
    #pg.draw.line(screen, (255,255,255), (0,0), (255,255), 3)
    for i in range(len(grid)):
        pane_left = grid_left+pane_size*(i%3)
        pane_top = grid_left+pane_size*(i//3)
        pg.draw.rect(screen, (255,255,255), (pane_left, pane_top, pane_size, pane_size))
        pane = pg.draw.rect(screen, (0,0,0), (pane_left+grid_line_width/2, pane_top+grid_line_width/2, pane_size-grid_line_width,pane_size-grid_line_width))
        if grid[i] == 1:
            screen.blit(maru_surface, (pane_left+pane_size/5, pane_top))
            #screen.blit(maru_surface, (pane_left, pane_top, pane_size, pane_size))
            #screen.blit(maru_surface, (pane_left, pane_top))
            #maru_surface.blit(screen, (pane_left, pane_top))
            # maru_surface.blit(pane, (0,0))
            #pg.draw.circle(screen, (255,0,0), (pane_left, pane_top), pane_size)
            #print("maru"):
        if grid[i] == -1:
            #screen.blit(batu_surface, (pane_left, pane_top, pane_size, pane_size))
            screen.blit(batu_surface, (pane_left+pane_size/5, pane_top))
            #print("batu")

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False


    keys = pg.key.get_pressed()

    for k, f in chars.items():
        key_const = getattr(pg, f"K_{k}")
        if keys[key_const]:
            screen.blit(chars[k], (300,300))
            

    pg.display.flip()
    clock.tick(60)

    frame_cnt += 1
    if frame_cnt>1090:
        running = False

print("display ended")
