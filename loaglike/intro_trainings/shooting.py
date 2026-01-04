import pygame as pg
import sys
import math

pg.init() #これはやらなくてもなぜか動いた（なんで）

screen = pg.display.set_mode((600, 500)) #これは初期化しないとそもそも fill できないので必要
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

# python は div とかいう概念がないので，毎回クラスを作る必要がある？
bullet_x = 0
bullet_y = 0
# この辺を，コントローラがあれば，右スティックで指定できたりしたらそれっぽい
# しかしながら，手頃なコントローラが存在しなくて詰んでいる
# w,a,s,d で方向指定できる可能性はあるが，流石に操作がむずい
# 2ボタンで順回転，逆回転ならばまあギリ操作ができるかもしれない
# 照準バーが必要になると思われ
bullet_dx = 0
bullet_dy = 0
bullet_speed = 10
bullet_r = 5
bullet_exist = False

# この辺，いろんなやつの初期化が本当にめんどくさいので，こういう時に継承とかが役立つのか？
# 正直そんな気もしないが？？まあいいや，答えは codex が知っているはずさ

# こういうのをクラス化しながら自然に描けるようになると，プログラミングが結構楽しくなると思う
# いまは，クラス化が下手くそすぎて，なんかコードをうつのが非効率に感じて気持ち悪いという問題がありそう
# きっと今までもそれを繰り返してきたのだろう，バカだな君は
enem_cx = 50
enem_cy = 50
enem_dx = 0
enem_dy = 0
enem_r = 50

# オブジェクトたちはもう一つの何かに入れておいて，毎回舐めるようにしたほうがわかりやすい？
# それが自然なのだが，できる限り汚くコーディングしてみたい，まずは
def fire():
    # global を入れないと動かなかった，まあグローバル変数に関数ないで値を代入するときは必須ということだろう
    # 多分，使用するだけなら問題ないはず (?)
    global bullet_x; bullet_x=cx
    global bullet_y;bullet_y=cy
    global bullet_dx;bullet_dx=0
    global bullet_dy;bullet_dy=-bullet_speed
    global bullet_exist;bullet_exist = True
    print("fire")
    

clear_flag = False
while running:
    screen.fill((0,0,0))
    #pg.draw.rect(screen, (0,0,255), (enem_cx-enem_r/2,enem_cy-enem_r/2,enem_cx+enem_r/2,enem_cy+enem_r/2))
    #pg.draw.rect(screen, (0,0,255), (enem_cx,enem_cy,enem_r,enem_r))
    rect = pg.Rect(0,0,enem_r,enem_r)
    rect.center = (enem_cx,enem_cy)
    pg.draw.rect(screen, (0,0,255),rect)
    pg.draw.circle(screen, (255,0,0), (cx, cy), 20)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False
            if event.key == pg.K_SPACE:
                fire()

    speed = 0.5 

    keys = pg.key.get_pressed()

    for k, f in chars.items():
        key_const = getattr(pg, f"K_{k}")
        if keys[key_const]:
            #print(key_const, pg.K_a)
            screen.blit(chars[k], (300,300))

    # direcs = ["UP", "DOWN", "LEFT", "RIGHT"]

    # なんかこの辺がループに全部入ってて，全てが２重ループになっているのが，
    # 著しく可読性を損なっている気がする，がまあ気にする必要はない (?)

    # とりあえずシューティングゲームを作ってみるか？
    # 自動で相手機を追尾する感じの．．．，まあそんなものすら自分で作ったことなかったとい作ったことなかったというのが驚きだが．
        if  keys[pg.K_UP]:
            #print("up")
            cy -= speed 
        if  keys[pg.K_DOWN]:
            #print("down")
            cy += speed
        if  keys[pg.K_LEFT]:
            #print("down")
            cx -= speed
        if  keys[pg.K_RIGHT]:
            #print("down")
            cx += speed
            
    # print(bullet_exist)
    # vim はコーディングが早くて楽しいというはなし
    # 全文置換は gg + V + G してからやらないといけないの？もっと楽な方法が欲しいが？
    # そんだけ面倒だったら，vscode の標準機能を使いたくなっちゃうよね？
    # javascript でテクい実装をしたくなってきた，python はだせえよ
    if bullet_exist:
        bullet_x += bullet_dx
        bullet_y += bullet_dy
        if bullet_x < 0 or bullet_x > screen.get_size()[0] or bullet_y < 0 or bullet_y > screen.get_size()[1]:
            bullet_exist = False
        #print(bullet_x, bullet_y)

        pg.draw.circle(screen, (255,255,255), (bullet_x, bullet_y), bullet_r)

    if bullet_y < enem_cy+enem_r/2 and bullet_y > enem_cy-enem_r:
        print("judge")
        if bullet_x < enem_cx+enem_r/2 and bullet_x>enem_cx-enem_r:
            #フォントの表示関数を作るのが異常にめんどくさい，元からあるんじゃね？
            print("hit")
            clear_flag=True
    if clear_flag:
        screen.blit(game_crear_surface, (300,300))
    
    if not clear_flag:
        enem_cx = int(screen.get_size()[0]/2 + (math.cos(frame_cnt/20) * screen.get_size()[0])/2)
        

    pg.display.flip() #これがないと赤くならない (画面の更新がないので当たり前)

    clock.tick(60)

    frame_cnt += 1
    if frame_cnt>1090:
        running = False

print("display ended")

# util とか作って，フォント表示とかをまとめたい感じがある
# キャラクターの abst 定義みたいなのも１箇所にまとめたい
# しかしながら，大規模化するビジョン，およびアイデアが見えていないので，すぐにはできなそう
# とりあえず，グリッドを作って動くようにしようか，パックマンも意外とサクッと作れるかも？？
# そもそも，コードを見ても考え方としてまとまってなくて気持ち悪いんだよな，だから後から見ても編集しにくいカスしよう
# 死ねカス

# やろうとすれば，3D 風味にもできるのかもしれない，pygame でできるのかは未知数ではあるが
# 今後の題材としては，3D シューティングとかはてぐせとしてはなかなか面白いかもしれない？？
# 意外と余裕でできてしまって焦ってる，やっぱり python は描きやすい，ただこの後拡張するのがマジで地獄だが．

# マス目移動を実現するか，ticktuk toe を作るか，3D シューティングを作るかの3択になっている
# 弾幕系のゲームにして，自機も打てるようにしたら面白いかも
# 自機が打つのは，最初のベクトルだけ，相手機に向けた感じにして，近づくほど当たりやすいという感じに
# さらに 3D にしたら超エキサイティングかもしれない？？いいね．
# もちろん，相手のヒット時の点滅とか，自機の HP 表示とかも必要
# これくらいの規模になってきたらそれなりの設計が必要になる気がする？結構自分プログラムの設計をするのは嫌いなんだが？まあいいか.

# 正直，書けば書くほどコーディングって上達するので，あんまり再利用する気がないのが問題な気がするんだが？
# 再利用可能なコーディングってどんな感じなんだろうか，クラスとかちゃんと完璧に（？）作ったら再利用する気は起きないんだろうか？
# まあでも，matplotlib とかまあ，tcpdump のやつは普通に再利用するきまんまんなので，物によるのかな