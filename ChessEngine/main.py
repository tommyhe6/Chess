from board import Board
from GUItk import GUI
import tkinter as tk
from PIL import ImageTk, Image

def main():
    root = tk.Tk()
    icon = ImageTk.PhotoImage(Image.open('../Imgs/icon.png'))
    root.tk.call('wm', 'iconphoto', root._w, icon)
    b = Board()
    g = GUI(root, b)
    g.draw_board()
    g.draw_pieces()
    g.pack(expand='true')
    root.mainloop()

if __name__ == '__main__':
    main()
