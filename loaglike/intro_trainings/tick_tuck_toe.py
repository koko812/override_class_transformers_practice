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

grid_row = 3

grid = [0] * (grid_row**2)
#grid[4] = 1
#grid[5] = -1
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
#maru_surface = marubatu_font.render("o",1,(255,255,255))
#batu_surface = marubatu_font.render("×",1,(255,255,255))
# どうやら font はサイズさえ合っていれば，使いまわせるっぽい，あとフォント体と
# surface はループの中で初期化した方が，色を変えられて便利そう
# その分ループが遅くなりそうなので，毎回初期化するのはいかがなものかという話で，何かしらの配列にためていきたいが

info_font = pg.font.Font(None, int(pane_size*0.7))

screen_w, screen_h = screen.get_size()

turn = 1
game_end = False
iswin = False

while running:
    screen.fill((0,0,0))
    # pg.draw.circle(screen, (255,0,0), (cx, cy), 20)
    if game_end:
        print("gameend")
        info_surface = info_font.render(f"turn: {turn}", 0, (255,255,255))
        if iswin:
            screen.fill((255,0,0))
        else:
            screen.fill((0,0,255))
    else:
        info_surface = info_font.render(f"turn: {turn}", 0, (255,255,255))
    info_surface = info_font.render(f"turn: {turn}", 0, (255,255,255))
    screen.blit(info_surface, (screen.get_width()-200, screen.get_height()-50))

    for i in range(len(grid)):
        mouse_pos = pg.mouse.get_pos()
        # print(mouse_pos[0])
        pane_left = grid_left+pane_size*(i%3)
        pane_top = grid_left+pane_size*(i//3)
        pg.draw.rect(screen, (255,255,255), (pane_left, pane_top, pane_size, pane_size))


        # 実装スピード（ロジック面）が早すぎて流石に笑う
        # これ，マジで何かに活かしたいところだが，一番偉いのはこれを使いまわせる構造を作ることなんだよなあ
        # ただ，このスピードが出るのは，明らかに javascript で結構ゲームの実装をしたからだよな，素晴らしい
        # ただまあ，こういうゴチャって作ったものを分解していくのが，真に合理的なやつなのかもしれない？？（そんなことないか）
        if mouse_pos[0] > pane_left and mouse_pos[0] < pane_left+pane_size and mouse_pos[1] > pane_top and mouse_pos[1] < pane_top + pane_size:
            if not game_end:
                pg.draw.rect(screen, (128,128,128), (pane_left+grid_line_width/2, pane_top+grid_line_width/2, pane_size-grid_line_width,pane_size-grid_line_width))
                # ここ，event_loop を本筋とは別に回しているが，大丈夫なのかという感じはある
                # 普通に event_loop をもっと早くに回して，そこでフラグに入れといた方が綺麗な気がする
                # 後，描画とロジックをもっと切り分けたい
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if grid[i] == 0:
                            grid[i] = turn % 2 * 2 -1
                            turn += 1
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
            
        # 結局，maru_surface の blit を使うんじゃなくて，screen やら，載せる下地の blit を使うということ
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

    # ここはまあ，一応まともに関数は使えてると思う
    # ただ，ここ以外にも，ディスプレイをするところとか，明らかに関数化したいのに，ぱっと見やり方がわからんから，
    # 諦めたという部分が何箇所かあったので，そこは技術不足だと言わざるを得ない
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

# マジでクラス構成とか終わりに終わってるんだが，でもロジックがなんとなく頭に入ってる＋ゲーム作りのループが頭に入ってる，のでなんとか作ることができるらしい（？）
# ただ，大規模化のスピードが終わるので，流石にこれはよくないと思う，でもクラスを使わずにどこまでできるのかは試してみたい
# 今試す時間は全くないので，定期的に試してみたいと思う，クラス使用禁止縛りでどこまでできるか
# 関数も禁止するとさらにめんどくさそうで逆に面白いかもしれん，C とか．．．でも流石に関数は最初からつけてるか．．？
# アセンブリとかまで落ちると，，，これも一応マクロあるからね，まあそれはオッケーとしよう

# 後追加するべきなものとしては，retry ボタンと quit ボタンかな，タイトルつけるなら，タイトルバックも入れたい
# 詰まるところ，ループを回せるようにしたいということ，この辺も一個のループにぶち込むのが流石に頭悪いのでどうにかしたい
# で，当たり前の機能として，CPU 対戦機能は盛り込みたい，これは easy, normal, hard で３種類入れられる．
# さらに，通信対戦機能とかもつけようと思ったらつけられる．この辺りを入れるとなってくると流石にクラスとか入れてちゃんと設計したい
# ... ただ，今深く悩むよりか，さっさと作るならば自分で考えながら作ってもそれなりにいけそうというのはわかってよかった．
# ... まあ，絶対 AI に書かせた方が綺麗だし早いということは言うまでもないのだけれど

# 流石に，ゲームエンドとかの分岐をどこにも同じように書くのが面倒なんだが，これはまとめられないんだろうか
# １００歩譲って，別に書くのは構わないんだけど，いろんな場所にバラバラに出てくるのがかなり読みづらい
# まあシンプルなのは，ゲームエンドの状態遷移を作って，そこに全部ぶち込むとまとまるけど，記述量が増えてキモいと言う問題もある

# maze みたいな環境を作るのも，なんとなく綺麗な実装で早く描けるようになる練習をしたい
# gymnasium とかに入っているものを綺麗に扱えるようになりたい．
# ... というか，まる罰ゲームなのに全く状態遷移チックに書く気がないのやばすぎでしょ？？ 状態遷移系の何かもちゃんと作りたい

# 技術が板についたら，流石にもうちょっとアイデア方面にも力を入れられそう，ということでゲーム作成を続けていきたい
# もっとややこしいゲームを作りたい
# なんか，状態遷移とかの型ができたら，それをいろんなゲームに使いまわせるようにはしておいた方が便利かもしれない