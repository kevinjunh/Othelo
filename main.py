import tkinter as tk
from othelo import OtheloGUI

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("オセロゲーム - スタート画面")

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="オセロゲーム", font=("Helvetica", 20))
        title_label.pack(pady=20)

        start_button = tk.Button(self.root, text="ゲームを開始", command=self.start_game)
        start_button.pack()

    def start_game(self):
        self.root.destroy()  # スタート画面を閉じる
        othello_game = OtheloGUI(tk.Tk())  # 新しいTkウィンドウを作成してゲームを開始
        othello_game.play()

if __name__ == "__main__":
    root = tk.Tk()
    start_screen = StartScreen(root)
    root.mainloop()
