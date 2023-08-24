import numpy as np

empty = 0
white = -1 
black = 1
wall = 9
board_size = 8
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
max_turns = 60

class Othelo:
    def __init__(self):
        self.raw_board = np.zeros((board_size + 2, board_size + 2), dtype=int)
        self.turns = 0
        self.current_color = black 
        self.raw_board[4, 4] = white
        self.raw_board[5, 5] = white
        self.raw_board[4, 5] = black
        self.raw_board[5, 4] = black
        self.init_canMove()

    def init_canMove(self):
        self.movablePosition = np.zeros((board_size + 2, board_size + 2, 8), dtype=bool)

        for x in range(1, board_size + 1):
            for y in range(1, board_size + 1):
                if self.raw_board[x, y] != empty:
                    continue

                for dir_idx, (dx, dy) in enumerate(directions):
                    if self.check_mobility(x, y, self.current_color, (dx, dy)):
                        self.movablePosition[x, y, dir_idx] = True

    def check_mobility(self, x, y, player, direction):
        dx, dy = direction
        x += dx
        y += dy

        if not (1 <= x <= board_size and 1 <= y <= board_size) or self.raw_board[x, y] != -player:
            return False

        while 1 <= x <= board_size and 1 <= y <= board_size:
            if self.raw_board[x, y] == empty:
                return False
            if self.raw_board[x, y] == player:
                return True
            x += dx
            y += dy

        return False

    def flip_discs(self, x, y, player, direction):
        dx, dy = direction
        x += dx
        y += dy

        while 1 <= x <= board_size and 1 <= y <= board_size:
            if self.raw_board[x, y] == empty or self.raw_board[x, y] == player:
                return

            self.raw_board[x, y] = player
            x += dx
            y += dy

    def move(self, x, y):
        if x < 1 or board_size < x or y < 1 or board_size < y:
            return False

        if self.raw_board[x, y] != empty:
            return False

        dir_idx = np.argmax(self.movablePosition[x, y])
        if not self.movablePosition[x, y, dir_idx]:
            return False

        self.flip_discs(x, y, self.current_color, directions[dir_idx])
        self.raw_board[x, y] = self.current_color
        self.turns += 1
        self.current_color = -self.current_color
        self.init_canMove()

        return True

    def game_over(self):
        if self.turns >= max_turns:
            return True

        if np.any(self.movablePosition):
            return False

        for x in range(1, board_size + 1):
            for y in range(1, board_size + 1):
                if self.raw_board[x, y] == empty:
                    for dir_idx, _ in enumerate(directions):
                        if self.check_mobility(x, y, self.current_color, directions[dir_idx]):
                            return False

        return True

    def skip(self):
        if np.any(self.movablePosition):
            return False

        if self.game_over():
            return False

        self.current_color = -self.current_color
        self.init_canMove()
        return True

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

    def input(self, inp):
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

    if not board.input(inp):
        print('正しい形式(例：f5)で入力してください')
        continue

    x = alphabet.index(inp[0]) + 1
    y = int(inp[1])

    if not board.move(x, y):
        print('そこには置けません')
        continue

    if board.game_over():
        board.display()
        print('ゲーム終了')
        break

    if not board.skip():
        continue

print()

count_black = np.count_nonzero(board.raw_board[:, :] == black)
count_white = np.count_nonzero(board.raw_board[:, :] == white)

print('```')
