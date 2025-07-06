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

        self.check_button = tk.Button(root, text="下一步检查 Q3", command=self.next_step_q3)
        self.check_button.pack()

        self.status_label = tk.Label(root, text="当前检查状态: j=0, i=0, k=1")
        self.status_label.pack()

        self.formula_label = tk.Label(root, text="当前检查公式:")
        self.formula_label.pack()

        self.step_state = {
            'j': 0,
            'i': 0,
            'k': 1
        }

    def draw_board(self, highlight_cells=None):
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(
                    j * CELL_SIZE, i * CELL_SIZE,
                    (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
                    fill=color
                )
                if highlight_cells and (i, j) in highlight_cells:
                    self.canvas.create_rectangle(
                        j * CELL_SIZE, i * CELL_SIZE,
                        (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
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
        self.board[row][col] ^= 1
        self.draw_board()

    def next_step_q3(self):
        j = self.step_state['j']
        i = self.step_state['i']
        k = self.step_state['k']

        self.status_label.config(text=f"当前检查状态: j={j}, i={i}, k={k}")
        self.formula_label.config(text=f"当前检查公式: ¬p({i},{j}) ∨ ¬p({k},{j})")

        self.draw_board(highlight_cells=[(i, j), (k, j)])

        if self.board[i][j] == 1 and self.board[k][j] == 1:
            messagebox.showerror("冲突", f"第 {j+1} 列的第 {i+1} 行和第 {k+1} 行同时有皇后！")
            return

        self.step_state['k'] += 1
        if self.step_state['k'] >= BOARD_SIZE:
            self.step_state['i'] += 1
            self.step_state['k'] = self.step_state['i'] + 1
        if self.step_state['i'] >= BOARD_SIZE - 1:
            self.step_state['j'] += 1
            self.step_state['i'] = 0
            self.step_state['k'] = 1

        if self.step_state['j'] >= BOARD_SIZE:
            messagebox.showinfo("通过", "所有列均满足 Q3 条件：每列至多一个皇后。")
            self.step_state = {'j': 0, 'i': 0, 'k': 1}
            self.status_label.config(text="当前检查状态: j=0, i=0, k=1")
            self.formula_label.config(text="当前检查公式:")
            self.draw_board()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("N 皇后问题 - Q3 步进式可视化检查")
    app = NQueensVisualizer(root)
    root.mainloop()