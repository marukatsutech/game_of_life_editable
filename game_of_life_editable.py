# Conway's Game of Life - editable (Tkinter, canvas)
import tkinter as tk
import numpy as np
import random
import copy


def boundary_row(n):  # Boundary condition
    if n >= row:
        return 0
    elif n < 0:
        return row - 1
    else:
        return n


def boundary_col(n):  # Boundary condition
    if n >= col:
        return 0
    elif n < 0:
        return col - 1
    else:
        return n


class Animation(tk.Tk):
    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        self.title("Conway's Game of Life - Click screen to switch cells")
        self.canvas = tk.Canvas(self, width=canvas_w, height=canvas_h, bg='white')
        self.canvas.bind('<ButtonPress-1>', self.switch_cell)
        self.button_switch = tk.Button(self, text='Run/Pause', command=lambda: self.switch_run_pause())
        self.button_step = tk.Button(self, text='Step', command=lambda: self.step_run())
        self.button_randomize = tk.Button(self, text='Randomize', command=lambda: self.randomise_cells())
        self.button_clear = tk.Button(self, text='Clear', command=lambda: self.clear_cells())
        self.sv = tk.StringVar()
        self.sv.set('Step=0')
        self.label_step = tk.Label(self, textvariable=self.sv)

        self.canvas.pack()
        self.button_switch.pack(side='left')
        self.button_step.pack(side='left')
        self.button_randomize.pack(side='left')
        self.button_clear.pack(side='left')
        self.label_step.pack(side='right')

        self.cells0 = np.zeros((row, col))  # Cells plane
        self.cells1 = np.zeros((row, col))  # Cells plane buffer

        self.is_run = False
        self.step = 0

    def clear_cells(self):
        for i in range(row):
            for j in range(col):
                self.cells0[i][j] = 0
                self.cells1[i][j] = 0
        self.draw_cells()
        self.step = 0
        self.sv.set('Step=' + str(self.step))

    def randomise_cells(self):
        for i in range(row):
            for j in range(col):
                self.cells0[i][j] = random.randint(0, 1)
        self.draw_cells()

    def draw_cells(self):
        self.canvas.delete('all')
        for i in range(row):
            for j in range(col):
                if self.cells0[i, j] == 1:
                    x = j * dot_pitch + offset
                    y = i * dot_pitch + offset
                    self.canvas.create_rectangle(x, y, x + dot_size, y + dot_size, fill='black')

    def run(self):
        while self.is_run:
            self.step += 1
            self.sv.set('Step=' + str(self.step))
            self.next_generation()
            self.draw_cells()
            self.canvas.after(20)
            self.canvas.update()

    def switch_run_pause(self):
        if self.is_run:
            self.is_run = False
        else:
            self.is_run = True
            self.run()

    def step_run(self):
        self.step += 1
        self.sv.set('Step=' + str(self.step))
        self.next_generation()
        self.draw_cells()

    def eval_neighbours(self, rw, cl):
        global cells0
        result = 0
        for k in range(8):
            result = result + self.cells0[boundary_row(rw + neighbours[k][0]), boundary_col(cl + neighbours[k][1])]
        return int(result)

    def next_generation(self):
        for i in range(row):
            for j in range(col):
                cell = self.cells0[i][j]
                result = self.eval_neighbours(i, j)
                if cell == 1:
                    if result < 2:
                        self.cells1[i][j] = 0
                    elif result == 2 or result == 3:
                        self.cells1[i][j] = 1
                    else:
                        self.cells1[i][j] = 0
                else:
                    if result == 3:
                        self.cells1[i][j] = 1
        # Reflect to cells0
        self.cells0 = copy.deepcopy(self.cells1)

    def callback(self, event):
        print("clicked at", event.x, event.y)
        self.canvas.delete('all')
        self.canvas.create_line(event.x, 0, event.x, 300, fill='black')
        self.canvas.create_line(0, event.y, 300, event.y, fill='black')

    def switch_cell(self, event):
        print("clicked at (x,y)", event.x, event.y)
        rw = (event.y - offset) // dot_pitch
        cl = (event.x - offset) // dot_pitch
        print("clicked at (row,col)", rw, cl)
        if 0 <= rw < row and 0 <= cl < col:
            if self.cells0[rw][cl] == 0:
                self.cells0[rw][cl] = 1
            else:
                self.cells0[rw][cl] = 0
            self.draw_cells()


# Global variables
dot_size = 6
gap_size = 2
dot_pitch = dot_size + gap_size
offset = 4
row = 50
col = 50
cells0 = np.zeros((row, col))   # Cells plane
cells1 = np.zeros((row, col))   # Cells plane buffer

canvas_w = dot_pitch * col + offset
canvas_h = dot_pitch * row + offset

# Relative row and column of neighbours
neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

anim = Animation()
anim.mainloop()
