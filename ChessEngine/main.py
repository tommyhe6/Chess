from board import Board
from GUItk import GUI
import tkinter as tk

def main():
    root = tk.Tk()
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='../Imgs/icon.png'))
    b = Board()
    g = GUI(root, b)
    g.draw_board()
    g.draw_pieces()
    g.pack(expand='true')
    root.mainloop()

if __name__ == '__main__':
    main()
