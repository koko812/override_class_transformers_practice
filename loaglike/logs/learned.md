# Pygame 学習メモ

ここまで学んだ内容を、後から見返しやすいように整理したメモです。
コードは最小例を中心に入れています。

## 画面表示の基本

ウィンドウ作成、メインループ、描画、画面更新の流れが基本です。

```python
import pygame as pg

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((30, 30, 30))
    pg.display.flip()
    clock.tick(60)
```

- `pg.display.set_mode` でウィンドウ作成
- `pg.display.flip()` で画面更新（これがないと描画が反映されない）

## 図形描画

### 円

```python
pg.draw.circle(screen, (255, 80, 80), (400, 300), 60)
```

引数は `(surface, color, center, radius)`。`width=0` なら塗りつぶし。

### 矩形

`pg.draw.rect` の第3引数は `(x, y, width, height)` で **左上座標＋幅高さ**。
中心座標を使うなら `Rect.center` を使うのが安全。

```python
rect = pg.Rect(0, 0, 50, 50)
rect.center = (cx, cy)
pg.draw.rect(screen, (0, 0, 255), rect)
```

左上として座標を渡すと、中心のつもりでもズレて見えるので注意。

## 文字表示

文字は「フォント → render → blit → flip」の流れ。

```python
pg.font.init()
font = pg.font.Font(None, 50)

text_surf = font.render("Hello", True, (255, 0, 0))
screen.blit(text_surf, (100, 100))
```

- `font` は **Fontクラスのインスタンス** が必要
- `Font(None, size)` の `None` は「デフォルトフォント」指定

### よくあるエラー

```text
TypeError: descriptor 'render' for 'pygame.font.Font' objects doesn't apply to a 'str' object
```

`font = pg.font.Font` のようにクラスを代入していると発生。
必ず `font = pg.font.Font(None, 50)` のようにインスタンス化する。

## キーボード入力

### 押された瞬間（KEYDOWN）

```python
for event in pg.event.get():
    if event.type == pg.KEYDOWN:
        print(event.key)
        if event.key == pg.K_SPACE:
            print("space")
```

### 文字として入力された値（unicode）

文字入力は `event.unicode` で取れる。
ただし文字キー以外は空になる。

```python
if event.type == pg.KEYDOWN:
    print(event.unicode)
```

### 押している間（長押し状態）

`pg.key.get_pressed()` は毎フレームの「押下状態」。

```python
keys = pg.key.get_pressed()
if keys[pg.K_a]:
    print("A is held")
```

### アルファベット全部を調べる

`getattr` で `K_a` などを文字列から取得できる。

```python
keys = pg.key.get_pressed()
for ch in "abcdefghijklmnopqrstuvwxyz":
    key_const = getattr(pg, f"K_{ch}")
    if keys[key_const]:
        print(ch, "pressed")
```

## 文字コード（Python）

```python
ord('a')  # 97
chr(97)   # 'a'
```

`int('a')` はエラーになるので注意。

## 描画が見えないときの典型原因

- `screen.blit(...)` の **後に** `pg.display.flip()` していない
- 描画順が逆（`flip` の後に `blit` している）

正しい順番:

```python
screen.fill((0, 0, 0))
screen.blit(text_surf, (100, 100))
pg.display.flip()
```

## 見た目のズレ・チラつき

上下の線がブレる原因は「小数座標 → int丸め」。
`Rect.center` を使うと内部の丸めが安定しやすい。
必要なら座標やサイズを `int` で揃えるのが有効。
