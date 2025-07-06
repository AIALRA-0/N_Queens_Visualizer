import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 4
CELL_SIZE = 60

class NQueensVisualizerQ5:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE)
        self.canvas.pack()

        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        self.canvas.bind("<Button-1>", self.place_queen)
        self.draw_board()

        self.check_button = tk.Button(root, text="下一步检查 Q5", command=self.next_step_q5)
        self.check_button.pack()

        self.status_label = tk.Label(root, text="当前检查状态: i=0, j=0, k=1")
        self.status_label.pack()

        self.formula_label = tk.Label(root, text="当前检查公式:")
        self.formula_label.pack()

        self.step_state = {'i': 0, 'j': 0, 'k': 1}

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(j*CELL_SIZE, i*CELL_SIZE, (j+1)*CELL_SIZE, (i+1)*CELL_SIZE, fill=color)
                if self.board[i][j] == 1:
                    self.canvas.create_text(j*CELL_SIZE + CELL_SIZE//2, i*CELL_SIZE + CELL_SIZE//2,
                                             text='♛', font=('Arial', 32), fill='red')

    def place_queen(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        self.board[row][col] ^= 1
        self.draw_board()

    def next_step_q5(self):
        i = self.step_state['i']
        j = self.step_state['j']
        k = self.step_state['k']

        max_k = min(BOARD_SIZE - i - 1, BOARD_SIZE - j - 1)

        if i >= BOARD_SIZE or j >= BOARD_SIZE - 1:
            messagebox.showinfo("通过", "所有主对角线均满足 Q5 条件：无冲突皇后。")
            self.step_state = {'i': 0, 'j': 0, 'k': 1}
            self.status_label.config(text="当前检查状态: i=0, j=0, k=1")
            self.formula_label.config(text="当前检查公式:")
            return

        if k > max_k:
            self.step_state['j'] += 1
            self.step_state['k'] = 1
            if self.step_state['j'] >= BOARD_SIZE - 1:
                self.step_state['i'] += 1
                self.step_state['j'] = 0
                self.step_state['k'] = 1
            self.next_step_q5()
            return

        i = self.step_state['i']
        j = self.step_state['j']
        k = self.step_state['k']
        i2 = i + k
        j2 = j + k

        self.draw_board()
        self.canvas.create_rectangle(j*CELL_SIZE, i*CELL_SIZE, (j+1)*CELL_SIZE, (i+1)*CELL_SIZE, outline='blue', width=3)
        self.canvas.create_rectangle(j2*CELL_SIZE, i2*CELL_SIZE, (j2+1)*CELL_SIZE, (i2+1)*CELL_SIZE, outline='blue', width=3)

        self.status_label.config(text=f"当前检查状态: i={i}, j={j}, k={k}")
        self.formula_label.config(text=f"当前检查公式: ¬p({i},{j}) ∨ ¬p({i2},{j2})")

        if self.board[i][j] == 1 and self.board[i2][j2] == 1:
            self.canvas.create_rectangle(j*CELL_SIZE, i*CELL_SIZE, (j+1)*CELL_SIZE, (i+1)*CELL_SIZE, outline='red', width=4)
            self.canvas.create_rectangle(j2*CELL_SIZE, i2*CELL_SIZE, (j2+1)*CELL_SIZE, (i2+1)*CELL_SIZE, outline='red', width=4)
            messagebox.showerror("冲突", f"第 {i+1},{j+1} 与 {i2+1},{j2+1} 同在主对角线上存在皇后！")
            return

        self.step_state['k'] += 1

if __name__ == '__main__':
    root = tk.Tk()
    root.title("N 皇后问题 - Q5 步进式可视化检查")
    app = NQueensVisualizerQ5(root)
    root.mainloop()