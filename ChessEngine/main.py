from board import Board
from GUItk import GUI
from draw import Draw
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
    d = Draw(root)
    g.pack(expand='true')
    d.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
