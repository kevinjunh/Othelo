import numpy as np

# マスの状態
empty = 0
white = -1 
black = 1
wall = 9

# ボードのサイズ
board_size = 8

# 方向
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# ボードの位置
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

# 手数の上限
max_turns = 60

# ゲームを管理するクラス
class Othelo:
    # ボードの初期化
    def __init__(self):
        # 空のボードを作成
        self.raw_board = np.zeros((board_size + 2, board_size + 2), dtype=int)

        # 手番数(ターン)
        self.turns = 0

        # 現在の手番の色(黒スタート)
        self.current_color = black 

        # 初期配置
        self.raw_board[4, 4] = white
        self.raw_board[5, 5] = white
        self.raw_board[4, 5] = black
        self.raw_board[5, 4] = black

        # 配置可能な位置を初期化
        self.init_canMove()

    # 配置可能な位置の初期化
    def init_canMove(self):
        self.movablePosition = np.zeros((board_size + 2, board_size + 2, len(directions)), dtype=bool)

        # ボード上の配置可能な位置を探索
        for x in range(1, board_size + 1):
            for y in range(1, board_size + 1):

                # 既に石がある場合はスキップ(配置不可)
                if self.raw_board[x, y] != empty:
                    continue

                # 全方向をチェックして、配置可能かどうかを判定
                for dir_idx, (dx, dy) in enumerate(directions):
                    if self.check_mobility(x, y, self.current_color, (dx, dy)):
                        self.movablePosition[x, y, dir_idx] = True

    # 特定の方向に対して石をひっくり返せるかをチェック
    def check_mobility(self, x, y, player, direction):
        dx, dy = direction
        x += dx
        y += dy

        # 最初のマスは相手の石
        if not (1 <= x <= board_size and 1 <= y <= board_size) or self.raw_board[x, y] != -player:
            return False

        # ２つ目以降のマスをチェック
        while 1 <= x <= board_size and 1 <= y <= board_size:
            if self.raw_board[x, y] == empty:
                return False
            
            if self.raw_board[x, y] == player:
                return True
            
            x += dx
            y += dy

        return False
    
    # 石をひっくり返す
    def flip_discs(self, x, y, player, direction):
        dx, dy = direction
        x += dx
        y += dy

        while 1 <= x <= board_size and 1 <= y <= board_size:
            if self.raw_board[x, y] == empty or self.raw_board[x, y] == player:
                return

            # 石をひっくり返す
            self.raw_board[x, y] = player
            x += dx
            y += dy
    

    # 石を配置
    def move(self, x, y):
        # 範囲外やすでに石がある場所(置けない)
        if x < 1 or board_size < x or y < 1 or board_size < y or self.raw_board[x, y] != empty:
            return False

        # 配置可能な方向がない場合(置けない)
        if not np.any(self.movablePosition[x, y]):
            return False

        # 石をひっくり返す
        for dir_idx, (dx, dy) in enumerate(directions):
            if self.movablePosition[x, y, dir_idx]:
                self.flip_discs(x, y, self.current_color, (dx, dy))

        # 石を置いてターンを進める
        self.raw_board[x, y] = self.current_color
        self.turns += 1
        self.current_color = -self.current_color

        # 配置可能な位置を更新
        self.init_canMove()

        return True


    # ゲーム終了判定
    def is_game_over(self):
        # ボードがいっぱい
        if self.turns >= max_turns:
            return True

        # まだ配置可能な場所がある場合はゲーム続行
        if np.any(self.movablePosition):
            return False

        # どちらのプレイヤーも置ける場所がない場合はゲーム終了
        return True
    

    # パスするメソッド
    def skip(self):
        # 配置可能な位置がある場合はパスできない
        if np.any(self.movablePosition):
            return False

        # ゲームが終了している場合はパスできない
        if self.is_game_over():
            return False
    
        # 手番を交代して配置可能な位置を更新
        self.current_color = -self.current_color
        self.init_canMove()
        return True


    # ボードの表示
    def display(self):
        print('  a b c d e f g h')
        for y in range(1, board_size + 1):
            print(y, end=" ")
            for x in range(1, board_size + 1):
                grid = self.raw_board[x, y]
                if grid == empty:
                    print('0', end=" ")
                elif grid == white:
                    print('2', end=" ")
                elif grid == black:
                    print('1', end=" ")
            print()


    # 入力のバリデーション
    def validate_input(self, inp):
        if not inp or len(inp) != 2:
            return False

        if inp[0] in alphabet and inp[1] in number:
            return True

        return False

# メイン
board = Othelo()

while True:
    board.display()

    player_color = '黒' if board.current_color == black else '白'
    inp = input(f'{player_color}の番です: ')
    print()

    if not board.validate_input(inp):
        print('正しい形式(例:f5)で入力してください')
        continue

    x = alphabet.index(inp[0]) + 1
    y = int(inp[1])

    if not board.move(x, y):
        print('そこには置けません')
        continue

    if board.is_game_over():
        board.display()
        print('ゲーム終了')
        break

    if not board.skip():
        continue

print()

count_black = np.count_nonzero(board.raw_board[:, :] == black)
count_white = np.count_nonzero(board.raw_board[:, :] == white)

print('```')
