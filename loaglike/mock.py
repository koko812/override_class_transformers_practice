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

# maru_font = pg.font.Font(None, int(pane_size*1.5))
# maru_surface = maru_font.render("o",1,(255,255,255))
# batu_font = pg.font.Font(None, int(pane_size*1.5))
# batu_surface = batu_font.render("×",1,(255,255,255))
marubatu_font = pg.font.Font(None, int(pane_size*1.5))
maru_surface = marubatu_font.render("o",1,(255,255,255))
batu_surface = marubatu_font.render("×",1,(255,255,255))
# どうやら font はサイズさえ合っていれば，使いまわせるっぽい，あとフォント体と

screen_w, screen_h = screen.get_size()

while running:
    screen.fill((0,0,0))
    pg.draw.circle(screen, (255,0,0), (cx, cy), 20)
    for i in range(len(grid)):
        mouse_pos = pg.mouse.get_pos()
        pane_left = grid_left+pane_size*(i%3)
        pane_top = grid_left+pane_size*(i//3)
        pg.draw.rect(screen, (255,255,255), (pane_left, pane_top, pane_size, pane_size))

        if mouse_pos[0] > pane_left and mouse_pos[0] < pane_left+pane_size and mouse_pos[1] > pane_top and mouse_pos < pane_top + pane_size
            pg.draw.rect(screen, (128,128,128), (pane_left+grid_line_width/2, pane_top+grid_line_width/2, pane_size-grid_line_width,pane_size-grid_line_width))
        else:
            pg.draw.rect(screen, (0,0,0), (pane_left+grid_line_width/2, pane_top+grid_line_width/2, pane_size-grid_line_width,pane_size-grid_line_width))

        if grid[i] == 1:
            screen.blit(maru_surface, (pane_left+pane_size/5, pane_top))
            
        # 結局，maru_surface の blit を使うんじゃなくて，screen やら，載せる下地の blit を使うということ
        if grid[i] == -1:
            screen.blit(batu_surface, (pane_left+pane_size/5, pane_top))

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

# タッチ判定は，基本的にペインごとに何かを持たせておくと楽なんだが？
# javascript だと，勝手に div を使うので，オブジェクト指向チックになって楽なんだろうか？
# それとも全然作ったことがないからよく作ったことがないからよくわかってことがないからよくわかってないのかどっちないからよくわかってないのかどっちなんだろうか
# onclick をつけるようにするから，やっぱりそれなりにオブジェクト指向っぽいことになってるんじゃないかと
# pane も div で宣言するので，白く色が変わるとかもいい感じにつけられるんだよね，Transform とかを使ってね
# しかしながら python や pygame にはそれが用意されてないので，まあまあめんどくさい，自分で定義しないといけないという話か
# なんか一回綺麗な python でのオセロとかその辺を真似したほうが早いような気がする？javascript はそれが染み付いてるので，やりやすいんだが
# ただ，その感覚が掴めたのならば，python でクラスを使うのも，そんなに違和感はないのかも
# そして，python でできたら，c とか java でもオブジェクト指向っぽい思考は使いまわせるということ，素晴らしい
# この辺で作った試作群を並べて表示する webページ的なものを作れたら，それなりに捗るような気がするが？
# streamlit とかを使ったら実現できないだろうか？流石に難しい？

# 何か web サービスの運用・保守経験は持っておいた方が絶対便利だな，さっさとやっちまおうかな
# それこそ，ハッカソンで作ったものをそのまま運用できればだいぶと楽なんだが？