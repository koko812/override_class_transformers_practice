import pygame as pg
import sys

pg.init() #これはやらなくてもなぜか動いた（なんで）

screen = pg.display.set_mode((600, 500)) #これは初期化しないとそもそも fill できないので必要
pg.display.set_caption("start this game!")

clock = pg.time.Clock()

running = True
frame_cnt = 0

pg.font.init()
font = pg.font.Font(None, 50)
chars = {chr(ord('a')+i):font.render(chr(ord('A')+i), 0, (255,0,0)) for i in range(ord('z')-ord('a')+1)}

cx = 100
cy = 100

while running:
    screen.fill((0,0,0))
    pg.draw.circle(screen, (255,0,0), (cx, cy), 20)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # if event.type == pg.KEYDOWN:
            # print(event.key)

            # 動くのは動くけど，押した瞬間しか動かない
            # if event.key == pg.K_UP:
            #     print("up")
            #     cy -= 1
            # elif event.key == pg.K_DOWN:
            #     print("down")
            #     cy += 1
            # elif event.key == pg.K_LEFT:
            #     print("down")
            #     cx -= 1
            # elif event.key == pg.K_RIGHT:
            #     print("down")
            #     cx += 1

    speed = 0.5 

    keys = pg.key.get_pressed()

    for k, f in chars.items():
        key_const = getattr(pg, f"K_{k}")
        if keys[key_const]:
            print(key_const, pg.K_a)
            screen.blit(chars[k], (300,300))

    # direcs = ["UP", "DOWN", "LEFT", "RIGHT"]
        if  keys[pg.K_UP]:
            print("up")
            cy -= speed 
        if  keys[pg.K_DOWN]:
            print("down")
            cy += speed
        if  keys[pg.K_LEFT]:
            print("down")
            cx -= speed
        if  keys[pg.K_RIGHT]:
            print("down")
            cx += speed
            

    pg.display.flip() #これがないと赤くならない (画面の更新がないので当たり前)

    clock.tick(60)

    frame_cnt += 1
    if frame_cnt>1090:
        running = False

print("display ended")

# とりあえず，四角の画面が出てきて，赤い丸が出てくるようにしよう
# あと，キーボードの受付がめんどくさいので，それは早めに設定しておこう，上下左右に動けるようにしよう
# スペースキーで剣を振れる感じにしよう，で，ターン制で敵が動ける or こっちの攻撃に応じて動くようにしてみよう