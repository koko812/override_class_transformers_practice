import pygame as pg
import colorsys
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("hello")

clock = pg.time.Clock()
runnning = True
loop_cnt = 0

minos_shapes = [[[0,-1],[0,1],[0,2]], # stick
                [[1,0],[0,1],[0,2]], # L
                [[1,0],[0,1],[1,1]], # block
                [[1,0],[0,1],[-1,1]], # z
                [[-1,0],[0,1],[1,1]], # 逆 z
                [[-1,0],[1,0],[0,1]],] # T

row = 20
col = 10


stage = None
def init_stage():
    global stage
    stage = [[0]*(col+2) for i in range(row+1)]
    stage[-1]=[9]*(col+2)
    for i in range(len(stage)):
        stage[i][0] = 9
        stage[i][-1] = 9

stage_height = 400
stage_width = 200
stage_top = (SCREEN_HEIGHT - stage_height)/2
stage_left = (SCREEN_WIDTH - stage_width)/2

def new_mino(pos:tuple, rotate=0, movable=1, mino_type=0):
    mino = {"pos": pos, "rotate": rotate, "movable": movable, "mino_type": mino_type}
    return mino

minos = []

def gen_mino():
    global minos
    mino_type = random.randint(0,5)
    mino = new_mino([5,0], 0, 1, mino_type)
    #print("gen_mino", mino)
    minos.append(mino)
    return mino

def matmul(a,b):
    # ゴミのような matmul で草
    # ただちょっとこれの方が for ループよりは早いのかも？？
    # この行列演算ミスでシステムが壊れたら流石にウケる
    return [[a[0][0]*b[0][0]+a[0][1]*b[1][0], a[0][0]*b[0][1]+a[0][1]*b[1][1]],
            [a[1][0]*b[0][0]+a[1][1]*b[1][0], a[1][0]*b[0][1]+a[1][1]*b[1][1]],]
    # 今気づいたが，相手は別に行列じゃなかった件について．．

def v_matmul(A,v):
    return [A[0][0]*v[0]+A[0][1]*v[1], A[1][0]*v[0]+A[1][1]*v[1]]

def rotate(shape, rot):
    rotate_mat = [[0,-1], [1,0]]
    for i in range(rot):
        for j in range(len(shape)):
            shape[j] = v_matmul(rotate_mat, shape[j])
            # ．．．流石にこの matmul とかをメインループにぶち込んで一個ずつ描く元気はねえ
            # でもインライン化とはそういうことをしているのかもしれない
    print(shape)
            
    return shape

def get_mino_top(mino):
    top = 0
    y = mino["pos"][1]
    blocks = rotate(minos_shapes[mino["mino_type"]], mino["rotate"]) # * rotate みたいな感じに入れたら多分しんどくない
    for _,dy in blocks:
        #print(y,dy)
        if y+dy>top:
            top = y+dy

    return top
        
def fall_mino():
    global minos
    for mino in minos:
        mx = mino["pos"][0]
        my = mino["pos"][1]
        ty = get_mino_top(mino)
        # これ，mino_top の判定だけじゃ，すり抜けが必ず起こるのでアウトですね？
        if mino["movable"]:
            if stage[ty+1][mx] == 0:
                mino["pos"][1] += 1
                return False
            else:
                mino["movable"] = False
                return True

def mino_show():
    init_stage()
    for mino in minos:
        x,y = mino["pos"]
        s = mino["mino_type"]
        stage[y][x] = s
        shape = rotate(minos_shapes[s], mino["rotate"])
        for dcod in shape:
            dx,dy = dcod
            stage[y+dy][x+dx] = s
        # x,y 座標が反転していたので死んでください
        # これをうまく扱う方法，ないっすかね？
        # stage の配列をそのまま扱ってるのがまずいのかもしれない？？
        # まあなんにせよ，ちょっとまともになったのでハッピーですよという話，いい話
        # あとは rotate の判定ですな，それと，move に関しても流石に愚直すぎなので，チェックはいれたい

        # このままだと，rotate を何個も入れる必要が出てきて多分面倒なのでどうにかしたい

def draw():
    pane_size = stage_width/10
    rect = pg.Rect(0,0,pane_size,pane_size)
    for i,row in enumerate(stage):
        for j,n in enumerate(row):
            rect_x = stage_left+j*pane_size - pane_size/2
            rect_y = stage_top+i*pane_size - pane_size/2
            rect_pos = (rect_x,rect_y)
            rect.topleft = rect_pos

            if n == 9:
                pg.draw.rect(screen, (128,128,128), rect)
            elif n == 0:
                pg.draw.rect(screen, (0,0,0), rect)
            else:
                color = colorsys.hsv_to_rgb((n-1)*0.15,0.8,0.8)
                color = tuple(int(x*255) for x in color)
                pg.draw.rect(screen, color, rect)
        
init_stage()
runnning = True
dropped = True

while runnning:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                mino["pos"][0] -= 1
            if event.key == pg.K_RIGHT:
                mino["pos"][0] += 1
            if event.key == pg.K_DOWN:
                mino["pos"][1] += 1 
            if event.key == pg.K_SPACE:
                mino["rotate"] = 1
        if event.type == pg.QUIT:
            runnning = False
                

    screen.fill((0,0,0))
    mino_show()
    draw()
    pg.display.flip()

    if dropped:
        mino = gen_mino()
        dropped = False

    if loop_cnt%10 == 0:
        dropped = fall_mino()

    clock.tick(30)
    if loop_cnt == 600:
        runnning = False
    loop_cnt+=1

print("end")

# 俺はテトリスの本質を分かってなかったようだ
# 完全に落ち切ったタイミングで次のミノが落ちてくるということを分かってなかったという，
# 圧倒的無知蒙昧，一回転生したほうがいいんじゃない？