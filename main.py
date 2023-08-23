import numpy as np

empty = 0
white = -1 
black = 1

board_size = 8

#ボードを表示
class Board:
    def __init__(self):

        #空のボード(石がない状態)
        self.rawBoard = np.zeros((board_size, board_size), dtype=int)

        
        #初期配置
        self.rawBoard[3, 3] = white
        self.rawBoard[4, 4] = white
        self.rawBoard[3, 4] = black
        self.rawBoard[4, 3] = black

        #ターン
        self.turn = 0

        #現在の手番の色
        self.currentColor = black

    def flip(self, x, y):

        #石を置く
        self.rawBoard[x, y] = self.currentColor


    #石を置く
    def move(self, x, y):
        
        #置く位置の確認
        if x < 0 or x > board_size:
            return False
        if y < 0 or y > board_size:
            return False

        
        #石裏返す(色を変える)
        self.flip(x, y)

        #手番を進める
        self.turn += 1

        #手番を交代する
        self.currentColor = -self.currentColor

        return True


#ボード作成
board = Board()

#move呼び出し
print(board.move(1, 1))

#ボード確認
print(board.rawBoard)
