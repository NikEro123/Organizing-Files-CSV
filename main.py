import tkinter as tk
from game import Game

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.resizable(False, False)

        self.game = Game()

        self.frame = tk.Frame(self.root, bg="#bbada0", bd=10)
        self.frame.pack()

        self.font = ("Helvetica", 24, "bold")

        self.cell_colors = {
            0: "#ccc0b3",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e"
        }

        self.cells = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        for i in range(4):
            for j in range(4):
                label = tk.Label(
                    self.frame,
                    text="",
                    font=self.font,
                    width=4,
                    height=2,
                    bg=self.cell_colors[0]
                )
                label.grid(row=i, column=j, padx=5, pady=5)
                self.cells[i][j] = label
        self.root.bind("<Key>", self.handle_key)

    def show_game_win(self):
        self.game_win_message = tk.Label(self.root, text="You win!", font=("Helvetica", 18), fg="red")
        self.game_win_message.pack(pady=10)

    def show_game_over(self):
        self.game_over_message = tk.Label(self.root, text="Game over!", font=("Helvetica", 18), fg="red")
        self.game_over_message.pack(pady=10)


        self.update_ui()

    def update_ui(self):
        for i in range(4):
            for j in range(4):
                value = self.game.grid[i][j]
                color = self.cell_colors.get(value, "#3c3a32")
                self.cells[i][j].config(
                    text=str(value) if value != 0 else "",
                    bg=color
                )

    def handle_key(self, event):
        key = event.char.lower()
        if key not in ['w', 'a', 's', 'd']:
            return

        old_grid = [row[:] for row in self.game.grid]

        if key == 'w':
            self.game.move_up()
        elif key == 's':
            self.game.move_down()
        elif key == 'a':
            self.game.move_left()
        elif key == 'd':
            self.game.move_right()

        if old_grid != self.game.grid:
            self.game.add_random_tile()
            self.update_ui()

        if self.game.is_game_won():
            self.show_game_win()
        elif self.game.is_game_over():
            self.show_game_over()
    
    def run(self):
        self.root.mainloop()

root = tk.Tk()
gui_game = GUI(root)
gui_game.run()

