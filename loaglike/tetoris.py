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
# ミノの用意ってどうしてたっけ？二重配列？
# となると 3重配列になるのか？流石にそれはややこしくないか？
# 相対座標で書いてた，確かに賢いね
# なんか最初に回転パターンの数字を入れてたわ，確かに賢い
# というか普通に 3重配列に入れてた，まあいいか

# これ，ステージはブロックがいっぱいあるようなそうていなのか？
# まあ，枠線がないと考えると，配置とかはちょっと楽な気がしないでもなちょっと楽なきがしないでもないけど
# テトリス単体のブロックとかをどうするかって話はちょっとあるような気もするけど
# ただそれは内側に何かしらのブロックを入れて影とか光をつければいいので，まあそんなにきにしなくても，という感じか

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
    print(stage)

# ステージの表示は普通にステージを舐めてくろい四角形を表示するだけでオッケー
# 枠線はどうしようかな，普通にセンチネル使ったほうが楽な気がするんだが？
# ミノがあるますは 1にするとかでいいんじゃなかろうか

# 論理設計と描画の設定は分けて書いたほうがわかりやすいという話
stage_height = 500
stage_width = 250
stage_top = (SCREEN_HEIGHT - stage_height)/2
stage_left = (SCREEN_WIDTH - stage_width)/2

#mino_x = 5
#mino_y = 5 

# 擬似的にはこうなりそうだが，ミノ自体には，rotate, pos, stopped みたいなのがありそうなので，
# 素直にクラスを作ったほうが楽な説が結構あるような気がするんだが，どんなもん？
def new_mino(pos:tuple, rotate=0, movable=1, mino_type=0):
    mino = {"pos": pos, "rotate": rotate, "movable": movable, "mino_type": mino_type}
    return mino

minos = []
# ... 普通に辞書型にするのが筋ってもんかな？
# mino 自体の辞書型を作るのか，それとも minos を辞書型で定義するのか
# まあ普通に考えて，mino を辞書型で定義したほうが絶対楽だし自然か

# とりあえずガンガン落ちてくるところまで実装してみるか
# これは流石に．．．mino オブジェクトを作ったほうが楽なのでは？

def gen_mino():
    global minos
    mino_type = random.randint(0,5)
    mino = new_mino([5,0], 0, 1, mino_type)
    print("gen_mino", mino)
    minos.append(mino)

def get_mino_top(mino):
    top = 0
    y = mino["pos"][1]
    blocks = minos_shapes[mino["mino_type"]]
    for _,dy in blocks:
        print(y,dy)
        if y+dy>top:
            top = y+dy

    return top
        
def fall_mino():
    global minos
    for mino in minos:
        mx = mino["pos"][0]
        my = mino["pos"][1]
        ty = get_mino_top(mino)
        if mino["movable"]:
            # print("mino_pos", mino["pos"])
            if stage[ty+1][mx] == 0:
                mino["pos"][1] += 1
            else:
                mino["movable"] = False

def mino_show():
    init_stage()
    for mino in minos:
        x,y = mino["pos"]
        s = mino["mino_type"]
        stage[y][x] = s
        shape = minos_shapes[s]
        for dcod in shape:
            dy,dx = dcod
            stage[y+dy][x+dx] = s
    
def draw():
    pane_size = stage_width/10
    rect = pg.Rect(0,0,pane_size,pane_size)
    for i,row in enumerate(stage):
        for j,n in enumerate(row):
            rect_x = stage_left+j*pane_size - pane_size/2
            rect_y = stage_top+i*pane_size - pane_size/2
            rect_pos = (rect_x,rect_y)
            rect.topleft = rect_pos
            # wall を細くしたほうがかっこいいが，めんどくさいので断念（？）
            # これも効率的に書く仕組みはあるはずなんだ
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

while runnning:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            pass

    screen.fill((0,0,0))
    mino_show()
    draw()
    pg.display.flip()

    if loop_cnt%10 == 0:
        fall_mino()

    if loop_cnt%90 == 0:
        gen_mino()

    clock.tick(30)
    if loop_cnt == 600:
        runnning = False
    loop_cnt+=1

print("end")


# 衝突判定が想像の 100倍くらい難しくてやばいんだが？
# いや，落ち着いて作ったら普通に作れるはずなんだが？そんなこともない気がするんだが？
# 悔しいけど，答え合わせをするしかないのか？否，一回ノートに書いて落ち着いて考えてみたいかもしれない？
# なんせ頭がぐるぐるして結構しんどい問題がある，シンの毒気にやられている．

# 前途多難だな．．．ぷよぷよもピンポンも作ろうと思ってたのに．．．
# 否，これでできたら他の言語でもできると考えてやるしかないのら！