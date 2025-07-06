import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 4
CELL_SIZE = 60

class NQueensVisualizer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE)
        self.canvas.pack()

        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        self.canvas.bind("<Button-1>", self.place_queen)
        self.draw_board()

        self.check_button = tk.Button(root, text="下一步检查 Q1", command=self.next_step_q1)
        self.check_button.pack()

        self.status_label = tk.Label(root, text="当前检查状态: i=0")
        self.status_label.pack()

        self.formula_label = tk.Label(root, text="当前检查公式:")
        self.formula_label.pack()

        self.i = 0

    def draw_board(self, highlight_row=None):
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(
                    j * CELL_SIZE, i * CELL_SIZE, (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE, fill=color
                )
                if highlight_row is not None and i == highlight_row:
                    self.canvas.create_rectangle(
                        j * CELL_SIZE, i * CELL_SIZE, (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
                        outline='blue', width=3
                    )
                if self.board[i][j] == 1:
                    self.canvas.create_text(
                        j * CELL_SIZE + CELL_SIZE // 2,
                        i * CELL_SIZE + CELL_SIZE // 2,
                        text='♛', font=('Arial', 32), fill='red'
                    )

    def place_queen(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        self.board[row][col] ^= 1  # toggle
        self.draw_board()

    def next_step_q1(self):
        i = self.i
        self.status_label.config(text=f"当前检查状态: i={i}")
        coord_clause = " ∨ ".join([f"p({i},{j})" for j in range(BOARD_SIZE)])
        self.formula_label.config(text=f"当前检查公式: {coord_clause}")

        self.draw_board(highlight_row=i)

        if not any(self.board[i][j] == 1 for j in range(BOARD_SIZE)):
            messagebox.showerror("未通过", f"第 {i+1} 行没有皇后，不满足 Q1 条件！")
            return

        self.i += 1
        if self.i >= BOARD_SIZE:
            messagebox.showinfo("通过", "所有行均满足 Q1 条件：每行至少一个皇后。")
            self.i = 0
            self.status_label.config(text="当前检查状态: i=0")
            self.formula_label.config(text="当前检查公式:")
            self.draw_board()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("N 皇后问题 - Q1 步进式可视化检查")
    app = NQueensVisualizer(root)
    root.mainloop()