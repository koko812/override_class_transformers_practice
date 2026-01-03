import pygame as pg
import random

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

grid_row = 3

grid = [0] * (grid_row**2)
grid_size = 300
grid_top = 100
grid_left = 100
grid_line_width = 3

panes = []
pane_size = grid_size//3

clear_flag = False

marubatu_font = pg.font.Font(None, int(pane_size*1.5))
info_font = pg.font.Font(None, int(pane_size*0.7))
menu_font_size = 40
menu_font = pg.font.Font(None, int(menu_font_size))
button_height = menu_font_size-10

screen_w, screen_h = screen.get_size()

turn = 1
game_end = False
iswin = False

# 外部からインポートしないとみづらい事件が発生するので，ファイルを分ける or 何かいい方法があるかも？
# 全部メイン文に集めるようにしたらマシになるかもしれない

# やっぱり関数の並べる順番がみづらいのが結構気になるのでどうにかしてほしい
# main 関数に全部入れる？となると，グローバル変数の扱いがめんどくさくなりそうなので，そこはどうにかしたいんだが
# js は多分そんなことないんだよな？？
def show_button(strs, x, y):
    global mouse_cliked
    global game_end
    global grid 
    global turn 
    global iswin
    global running
    button_height = menu_font_size -10 
    button_width = (menu_font_size-15) * len(strs)
    b_rect = pg.Rect(x+5,y+5, button_width, button_height)
    b_rect.topleft = (x+5,y+5)
    f_rect = pg.Rect(x,y,button_width, button_height)
    f_color = (200,200,200)
    button_surface = menu_font.render(f"{strs}", 0, (0,0,0))
    if ismouseinRect(f_rect):
        f_rect.topleft = (x+2, y+2)
        button_topleft = (x+20+2, y+5+2)
        if mouse_cliked:
            f_color = (128,128,128)
            # init メソッドは作った方が絶対に便利だと思う
            game_end = False
            iswin = False
            grid = grid_row ** 2 * [0]
            turn = 0
            if strs == "end":
                running = False
    else:
        f_rect.topleft = (x,y)
        button_topleft = (x+20, y+5)
    pg.draw.rect(screen, (64,64,64), b_rect)
    pg.draw.rect(screen, f_color, f_rect)
    screen.blit(button_surface, button_topleft)

# 型宣言，インテリセンスが便利すぎるぅ
# isclicked 関数みたいな，高階関数をぶち込めれば，結構便利な気がするが？
# それこそ，javascript 的な
def ismouseinRect(rect:pg.Rect):
    top = rect.top
    left = rect.left
    height = rect.height
    width = rect.width
    global mouse_pos; mousepos = mouse_pos
    x = mousepos[0]
    y = mousepos[1]
    #print(top,left,height,width,mousepos)

    if y > top and y < top + height and x > left and x < left + width:
        #print("inrect")
        return True
    else:
        #print("norect")
        return False

#game_end = True

mouse_cliked = False
mouse_flag = 0

# とりあえず cpu は何を使わせるのかという話で．
# とりあえず idx を返すという感じにすればいいんじゃないかと思う
# これを大規模化するのが大変だという話
# まあ，このやり方はどう足掻いても練習しないと身につかないので，練習するしかないという話なんだがね
# たーだぁ，コードをあと増やそうとすると，CPU のパターンと，タイトル画面の難易度選択くらい？
# とすると，状態遷移的なのがもうちょっと増えることになると思うんだけど

# もはや，設計を専門に一回がっつり学んでみるのもありなのかもしれない，デザインパターンとかもね？？

def cpu_random_choice():
    global grid
    #random.choice()
    choiced = 0
    puttable = 0
    for g in grid:
        if g==0:
            puttable = 1
        
    if not puttable:
        return -1

    while True:
        idx = random.randrange(len(grid))
        if grid[idx] == 0:
            choiced = 1
        if choiced:
            break
    
    return idx

while running:
    # なぜかここにクリック判定チェックを入れると反応しなくなる 
    # for event in pg.event.get():
    #     if event.type == pg.MOUSEBUTTONDOWN:
    #         mouse_cliked = True
    #         print("clicked")

    screen.fill((0,0,0))
    mouse_pos = pg.mouse.get_pos()
    #print(mouse_pos)

    if game_end:
        info_surface = info_font.render(f"turn: {turn}", 0, (255,255,255))
        if iswin:
            screen.fill((255,0,0))
        else:
            screen.fill((0,0,255))
        show_button("retry", screen.get_width()-150, screen.get_height()-450)
        show_button("end", screen.get_width()-150, screen.get_height()-400)
        turn = 1

    else:
        info_surface = info_font.render(f"turn: {turn}", 0, (255,255,255))
    info_surface = info_font.render(f"turn: {turn}", 0, (255,255,255))
    screen.blit(info_surface, (screen.get_width()-200, screen.get_height()-50))

    cpu_choiced = cpu_random_choice()

    for i in range(len(grid)):
        pane_left = grid_left+pane_size*(i%3)
        pane_top = grid_left+pane_size*(i//3)
        pg.draw.rect(screen, (255,255,255), (pane_left, pane_top, pane_size, pane_size))

        if mouse_pos[0] > pane_left and mouse_pos[0] < pane_left+pane_size and mouse_pos[1] > pane_top and mouse_pos[1] < pane_top + pane_size:
            if not game_end:
                pg.draw.rect(screen, (128,128,128), (pane_left+grid_line_width/2, pane_top+grid_line_width/2, pane_size-grid_line_width,pane_size-grid_line_width))
                if turn%2 == 1:
                    for event in pg.event.get():
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if grid[i] == 0:
                                grid[i] = turn % 2 * 2 -1
                                turn += 1
                else:
                    pg.time.delay(300)
                    grid[cpu_choiced] = turn % 2 * 2 -1
                    turn+=1
                    
            else:
                pg.draw.rect(screen, (0,0,0), (pane_left+grid_line_width/2, pane_top+grid_line_width/2, pane_size-grid_line_width,pane_size-grid_line_width))
        else:
            pg.draw.rect(screen, (0,0,0), (pane_left+grid_line_width/2, pane_top+grid_line_width/2, pane_size-grid_line_width,pane_size-grid_line_width))

        if grid[i] == 1:
            if iswin:
                maru_surface = marubatu_font.render("o",1,(255,255,0))
            else:
                maru_surface = marubatu_font.render("o",1,(255,255,255))
                
            screen.blit(maru_surface, (pane_left+pane_size/5, pane_top))
            
        if grid[i] == -1:
            if (not iswin) and game_end:
                batu_surface = marubatu_font.render("x",1,(0,255,255))
            else:
                batu_surface = marubatu_font.render("x",1,(255,255,255))
            screen.blit(batu_surface, (pane_left+pane_size/5, pane_top))


    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_cliked = True
            mouse_flag = frame_cnt + 10

    # こんな感じの delay イベント実行がうまくできたらだいぶと楽なんじゃないかと思う
    if mouse_flag < frame_cnt:
        #print(mouse_flag, frame_cnt)
        mouse_cliked = False
            
    # game_end_judge
    def isWin(a,b,c):
        global iswin
        global game_end

        if a+b+c == 3:
            game_end=True
            iswin=True
        elif a+b+c == -3:
            game_end=True
            iswin=False

    for i in range(len(grid)):
        if i//3 == 0:
            isWin(grid[i],grid[i+3],grid[i+6])
            if i%3 == 0:
                isWin(grid[i],grid[i+4],grid[i+8])

        if i%3 == 0:
            isWin(grid[i],grid[i+1],grid[i+2])
            if i//3 == 2:
                isWin(grid[i], grid[i-2], grid[i-4])

    keys = pg.key.get_pressed()

    for k, f in chars.items():
        key_const = getattr(pg, f"K_{k}")
        if keys[key_const]:
            screen.blit(chars[k], (300,300))
            
    pg.display.flip()
    clock.tick(30)

    frame_cnt += 1
    if frame_cnt>1090:
        running = False
print("display ended")

# あとは，マス目移動系のロジックを書いてみたいんだが？
# まあ要するに，．．．という話？？（何言ってんだ？）
# ゲームをいつも再利用しないのは，多分ロジックが結構柔軟でしかも，結構難しいからなんだろうか
# 一回どっかに手順書的なのをまとめたら，この再利用しない病ももうちょっと改善するのかもしれない（？） 
# あり得るね，マジで頭の整理ができてないから，こんなことになってるのかもしれない，バカすぎる

# まあ，拡張はその２方向だなあ，という感じ
# 次なるアイデアとしては，これをマス目ごとに動くようなローグライクにするか，
# 他のマス目移動ゲーを作ってみるか，その他の何かを作ってみたい？
# まあもうちょっと，マス目の拡張が容易になるような実装にしたいような気がする

# うーん，グリッドをものとして扱う方法がいまいちパパッと思いつかないところで困る
# グリッドの描画がとにかく重すぎるんだよなあ，いやまあそれはfunction に分けたら問題ないか
# ただ，結構色々関数みたいなのが詰まってるので，（dense に結合してるので）結構そこがときほぐしづらい問題がある
# いやーマジでどうすればいいんだろうか？

# とはいえ，こうやってみてみると，あまりにも決めるべき変数が多すぎるんだよなあ
# こんなに色々なパラメータをいじるのは大変なので，そこはあうまく設定したいという話がある