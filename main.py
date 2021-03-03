from Engine.board import Board
from Engine.GUItk_AI import GUI
from Engine.draw import Draw
import Engine.info
import tkinter as tk
from PIL import ImageTk, Image
import chess

if __name__ == "__main__":
    COLOR = input("Enter color (w or b): ")
    Engine.info.COLOR = COLOR
    root = tk.Tk()
    icon = ImageTk.PhotoImage(Image.open('Imgs/icon.png'))
    root.tk.call('wm', 'iconphoto', root._w, icon)
    b = Board()
#     b_AI = chess.Board.mirror(chess.Board())
    b_AI = chess.Board()
    g = GUI(root, b, b_AI)
    g.draw_board()
    g.draw_pieces()
    d = Draw(root)
    g.pack(expand='true')
    d.pack()
    root.mainloop()

