import tkinter as tk
from tkinter.font import Font
import time

class Draw(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        white = tk.Button(text='Draw\nWhite', command=self.white_press)
        white.pack(side='top')
        black = tk.Button(text='Draw\nBlack', command=self.black_press)
        black.pack(side='bottom')
        self.white_time = -6
        self.black_time = -12

    def white_press(self):
        self.white_time = time.time()
        self.check_end()

    def black_press(self):
        self.black_time = time.time()
        self.check_end()

    def check_end(self):
        if abs(self.white_time - self.black_time) < 5:
            draw_root = tk.Tk()
            draw_root.geometry('500x500')
            draw_root.resizable(0, 0)
            text = tk.Text(draw_root)
            text.insert(tk.INSERT, 'Draw!')
            text.configure(font=Font(size=30))
            text.pack()
            draw_root.mainloop()

