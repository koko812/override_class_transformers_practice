import pygame as pg

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("hello")

clock = pg.time.Clock()
runnning = True
loop_cnt = 0

grid_row_length = 6
grid_states = [0] * grid_row_length ** 2
grid_states[0] = 1
grid_states[grid_row_length**2-1] = 3
grid_states[grid_row_length*2-3] = 9
grid_states[grid_row_length*3-4] = 9
grid_states[grid_row_length*4-4] = 9
print(grid_states)

grid_size = 500
grid_left = (SCREEN_WIDTH - grid_size)//2
grid_top = (SCREEN_HEIGHT - grid_size)//2
# grid のサイズを変えて，pane は grid_size によって自動的に決まるようにした方が便利か？
pane_size = grid_size//grid_row_length

player_pos = 0

def draw_grid():
    for i,s in enumerate(grid_states):
        left = grid_left+pane_size*(i%grid_row_length)
        top = grid_top+pane_size*(i//grid_row_length)
        line_width = 4
        outer_pane = pg.Rect(left, top, pane_size, pane_size)
        inner_pane = pg.Rect(left+line_width//2, top+line_width//2, pane_size-line_width, pane_size-line_width)
        #pg.draw.rect(screen, (255,255,255), outer_pane)
        pg.draw.rect(screen, (0,0,0), outer_pane)

        if s == 3:
            pg.draw.rect(screen, (0,255,0), inner_pane)
        elif s == 9:
            pg.draw.rect(screen, (64,128,128), inner_pane)
        else:
            pg.draw.rect(screen, (0,0,0), inner_pane)

        if i == player_pos:
            cx = left + pane_size / 2
            cy = top + pane_size / 2
            radius = 30
            pg.draw.circle(screen, (255,0,0), (cx,cy), radius)

key_to_dir = {pg.K_LEFT:-1, pg.K_DOWN:grid_row_length, pg.K_RIGHT:1, pg.K_UP:-grid_row_length}

# ここの判定がやっぱりめんどくさいしダサいんだよなあ，いやうまく動いてるのはすごいとは思うんだけど
def move_player(event_key):
    global grid_states
    global player_pos

    dir = key_to_dir[event_key]
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
        
    if grid_states[player_pos+dir] == 9:
        dir = 0

    player_pos += dir


while runnning:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            # 攻撃とかのモーションをつけるとなると，move 一括で player に受け取らせて振る感じの方がいいかも？
            # この部分で，キーの判別とかをあんまりしたくない感じがする
            move_player(event.key)

    screen.fill((0,0,128))
    draw_grid()
    pg.display.flip() #これは必須（2回目）

    clock.tick(30)
    if loop_cnt == 300:
        runnning = False
    loop_cnt+=1

print("end")

# ここからどうしようかと思ってるんだが，まあ敵を出すのは鉄板らしい，まあそうか
# 敵がこっちを追尾してくるアルゴリズムはまあまあ難しそう
# 剣を振る，攻撃するというモーションもつけた方が良さそう
# 経過したターン数とかも上に表示されるようにしたい（この辺をいつも書くのがめんどくさいので，楽に描けるようにしたい）
# もちろん HP もね．敵キャラクターの上に HP バーが表示されるようにできれば面白いかも
# もうちょっとステージを充実させたい感じはあるかもしれない
# ...というか，これをさっさとリリースして保守するということを，今年度中にやりたいんだが？
# できればもうちょっと数学的要素を使った何かのアプリをリリースしたいところなんだが，難しそうではある

# マップの自動生成とかできたらまあ楽しそうではあるんだが
# もうちょっと不思議ダンジョンっぽい形にしたい感じはあるかも？
# ダンジョンの形がつまらねえんだよな，ただ，ダンジョンのエリア移動みたいなのは結構実装が難しそう
# HPバーとか，ターン数とか，満腹ゲージとかの実装が地味に重そう
# こういうのは，画面のヘッダーとかフッターとかそういうものの区分けをした方がいいかも？ 
# そもそも，自分でステージを書くのが大変なんだよな，いやまああとでマップから読み込めるようにしたら，そうでもないのかも？
# その辺の自動生成を AI がやってくれたら嬉しいのになあ
# ...じゃなくて，その辺も自分でいい感じにルールをつけて自動生成するようにしたらいいと思うんだけど

# 8番出口みたいな（？知らんけど）3D 視点の不思議ダンジョンとかも結構おもろいかもしれない？
# 敵がこっちの動きを予測して追尾するみたいなのもあったら相当すごいと思う
# まあ，実装がクソ難しそうなんで，流石にきついかなあという感じがするんだが
# 今日の目標を定めよう．今日は HPバーと MPバー，そして満腹ゲージの実装
# で，敵の動きの実装，さらに．．．，敵との攻撃のやり合いの実装をしたい
# 加えて，タイトルページの実装，終了ページの実装，できればランキングページの実装
# ... となると，タイピングゲームみたいなものの実装もしたいんだけど
# 敵とリアルタイムに対戦する何かの実装もしてみたい，これはちょっとすぐにはアイデアが思いつかんが．．．
# もうちょっと俯瞰して眺める感じの角度の実装にもしてみたいんだが，この辺はロジックが完成したあとでもいいと思う

# ...というかそれは，ホッケーゲームを敵の行動をサーバーに投げさせる形式にしたら，擬似的には再現できるのでは？という感じ
# うーん，落ちもの系を高速で今から作るか，これを進めていくかのどっちかになる感じがする
# どっちがいいんだろう，オセロも作りたいんだけど．なんか，基礎が固まってないので，どれを作るにもまあまあ疲れちゃう問題があるんだよなあ
# ただまあ，作るたびになんか構成の仕方とか，作る順番とかがわかってくるので，早くなって負担も減ってくる感じがあって，そこは悪くないと思うんだけど

# 俺が今作れるのって，オセロと，シューティングと，リアクター？（あれは結構難しい）倉庫番（アルゴリズムが難しい）くらいかなあ
# ただこの辺に関しては，アルゴリズムは難しいんだが，それなりに時間をかけて考えると作れなくはないというレベルなんだよな
# でまあ，時間をかけたら C でも似たようなものを作れるという実感はちょっとだけある，まあ時間かかりそうだが
# あんまり言語にいぞんしないというか，自分的に lang agnostic に作れるのは強みなんじゃないかと思うんだけど
# まあ，もっともっといろんな言語を触ってみたいという気持ちは尽きないんだけど
# パワーショット可能，カーブ可能なホッケーとか今までにあんまりなくて面白いかも？少なくとも自分はすきだな
# パワーショットにアニメーション付けな難しそうだし，タイミングがややこしそうだけど
# あと，パワーショットばっかり作ってたら，ショットのスピードが異次元に上がりそうなので，そこは気をつけたいところ
# ちょっとその方面で一旦 2D で作ってみようかな？？
# 棒じゃなくて，普通にパックにしてみるのもいいかも？まあ実装が普通に重くなりそう，というか数学的なアレが重くなりそうな気がするが