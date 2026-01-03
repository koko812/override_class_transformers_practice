import pygame as pg

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("hello")

clock = pg.time.Clock()
runnning = True
loop_cnt = 0

# 初期化と何かの更新は分けた方がいいような気がする
# というか，クラスにすれば管理しやすいのだと思う，react の state とかもそうなんだろうか
grid_row_length = 4
grid_states = [0] * grid_row_length ** 2
grid_states[0] = 1
grid_states[grid_row_length**2-1] = 3
print(grid_states)

grid_left = 100
grid_top = 100
pane_size = 100

player_pos = 0

def draw_grid():
    for i,s in enumerate(grid_states):
        left = grid_left+pane_size*(i%grid_row_length)
        top = grid_top+pane_size*(i//grid_row_length)
        line_width = 4
        outer_pane = pg.Rect(left, top, pane_size, pane_size)
        inner_pane = pg.Rect(left+line_width//2, top+line_width//2, pane_size-line_width, pane_size-line_width)
        pg.draw.rect(screen, (255,255,255), outer_pane)

        if s == 3:
            pg.draw.rect(screen, (0,255,0), inner_pane)
        else:
            pg.draw.rect(screen, (0,0,0), inner_pane)

        if i == player_pos:
            cx = left + pane_size / 2
            cy = top + pane_size / 2
            radius = 30
            pg.draw.circle(screen, (255,0,0), (cx,cy), radius)

# left とかの辞書を作りたいもんだが，いまいちメリットがわからん
# ので，とりあえず 1,2,3,4 でいいや
# 境界チェックがちょっとめんどくさいかも？
# センチネルの方が実装は早いかもしれん？慣れているならば
# 1次元配列で操作するのが思ったよりも面倒かもしれないという話

key_to_dir = {pg.K_LEFT:-1, pg.K_DOWN:grid_row_length, pg.K_RIGHT:1, pg.K_UP:-grid_row_length}

# ちょっとこの関数は微妙な感が強い，がもうちょっと頑張りたい．
# まあ少なくとも，grid を global で扱いたくない
# player_pos と grid_state は分けて扱った方が良いのか？
# ひとまず，bit_flag とかにしないと，ゴールマスを通った時に player_state に塗り替えられるので，
# ひとまず分離する形にしたが，後々ループを player_pos と grid_state に二重に回す必要が出てくるとするとめんどくさい
def move_player(event_key):
    global grid_states
    global player_pos

    dir = key_to_dir[event_key]
    #player_pos = grid_states.index(1)
    if dir==-1:
        if player_pos%(grid_row_length)==0:
            dir = 0
    if dir==grid_row_length:
        if player_pos//(grid_row_length)==grid_row_length-1:
            dir = 0
    if dir==1:
        if player_pos%(grid_row_length)==grid_row_length-1:
            dir = 0
    if dir==-grid_row_length:
        if player_pos//(grid_row_length)==0:
            dir = 0

    player_pos += dir

while runnning:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            move_player(event.key)

    screen.fill((0,0,255))
    draw_grid()
    pg.display.flip() #これは必須（2回目）

    clock.tick(30)
    if loop_cnt == 300:
        runnning = False
    loop_cnt+=1

print("end")