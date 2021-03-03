from Engine.board import Board
import Engine.AI
import Engine.info
import tkinter as tk
from tkinter.font import Font
import os
import copy
from PIL import ImageTk, Image
import time

ROWS = 8
COLS = 8
SQUARE_SIZE = 64
WIDTH = ROWS * SQUARE_SIZE
HEIGHT = COLS * SQUARE_SIZE

#TODO non-queen pawn promotion

def other(color):
    return 'w' if color == 'b' else 'b'

def pos_to_pixel(pos, x, y):
    x[0] = pos[0] * SQUARE_SIZE
    x[1] = x[0] + SQUARE_SIZE
    y[0] = pos[1] * SQUARE_SIZE
    y[1] = y[0] + SQUARE_SIZE


class GUI(tk.Frame):
    def __init__(self, root, board, board_AI):
        tk.Frame.__init__(self, root)
        self.root = root
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(side='top', fill='both', expand='true')
        self.canvas.bind('<Button-1>', self.click)
        self.board = board
        self.board_AI = board_AI
        self.moves_shown = False
        self.last = {}
        self.turn = 'w'
        self.prev_moves = []
        self.res = (False, None, None)

    def draw_board(self):
        for x in range(COLS):
            for y in range(ROWS):
                x_pix = [0, 0]
                y_pix = [0, 0]
                pos_to_pixel((x, y), x_pix, y_pix)
                self.canvas.create_rectangle(x_pix[0], y_pix[0], x_pix[1], y_pix[1], fill='navajo white' if (x+y)%2==0 else 'burlywood3', outline='black')

    def draw_pieces(self):
        all_pieces = []
        for color in self.board.pos_pieces:
            i = 0
            for pos, piece in self.board.pos_pieces[color].items():
                p = ImageTk.PhotoImage(Image.open('Imgs/{}.png'.format(repr(piece))).convert('RGBA'))
                self.canvas.create_image(SQUARE_SIZE * (pos[0]+1/2), SQUARE_SIZE * (pos[1]+1/2), image=p)
                all_pieces.append(p)
        self.canvas.images = all_pieces

    def get_piece(self, pos):
        if pos in self.board.pos_pieces['w']:
            return self.board.pos_pieces['w'][pos]
        elif pos in self.board.pos_pieces['b']:
            return self.board.pos_pieces['b'][pos]
        else:
            return None

    def get_coords(self, event):
        return (event.x//64, event.y//64)

    def draw_moves(self, moves):
        R = 10
        moves = [(SQUARE_SIZE * (i[0]+1/2), SQUARE_SIZE * (i[1]+1/2)) for i in moves]
        self.moves_drawn = []
        for x, y in moves:
            self.moves_drawn.append(self.canvas.create_oval(x-R, y-R, x+R, y+R, fill='Azure', width=0))

    def win(self, color):
        win_root = tk.Tk()
        win_root.geometry('500x500')
        win_root.resizable(0, 0)
        text = tk.Text(win_root)
        text.insert(tk.INSERT, '{} won!'.format(color))
        text.configure(font=Font(size=80))
        text.pack()
        win_root.mainloop()

    def click(self, event):
        pos = self.get_coords(event)
        piece = self.get_piece(pos)
        self.res = (False, None, None)
        if Engine.info.COLOR != self.turn:
            (val, move_uci) = Engine.AI.minimax_AB(3, self.board_AI, True, self.turn)
            self.board_AI.push(move_uci)
#             print(self.board_AI)
#             print(self.board.pos_pieces)
#             print(move_uci)
            move = Engine.AI.uci_to_mv(move_uci)
#             print(move[0], move[1])
            self.board.move(move[0], move[1])
            self.draw_pieces()
            self.turn = other(self.turn)
            
        if not self.moves_shown:
            if piece is not None and piece.color == self.turn and Engine.info.COLOR == self.turn:
                self.draw_moves(piece.show_moves(pos))
                x = [0, 0]
                y = [0, 0]
                pos_to_pixel(pos, x, y)
                self.moves_drawn.append(self.canvas.create_rectangle(x[0], y[0], x[1], y[1], outline='firebrick1', width=2))
                self.moves_shown = True
                self.last['pos'] = pos
                self.last['piece'] = piece
        else:
            if pos in self.last['piece'].show_moves(self.last['pos']):
                board_temp = copy.deepcopy(self.board)
#                 print(self.last['pos'], pos)
                board_temp.move(self.last['pos'], pos)
                if not board_temp.in_check(self.turn):
                    self.board = board_temp
                    self.board_AI.push(Engine.AI.mv_to_uci((self.last['pos'], pos)))
                    self.turn = other(self.turn)
                    self.res = (True, self.last['pos'], pos)
                if self.last['pos'] != None:
                    [self.canvas.delete(i) for i in self.prev_moves]
                    self.prev_moves = []
                    x = [[0, 0], [0, 0]]
                    y = [[0, 0], [0, 0]]
                    pos_to_pixel(self.last['pos'], x[0], y[0])
                    pos_to_pixel(pos, x[1], y[1])
                    for i in range(2):
                        self.prev_moves.append(self.canvas.create_rectangle(x[i][0], y[i][0], x[i][1], y[i][1], outline='light sky blue', width=3))
            [self.canvas.delete(i) for i in self.moves_drawn]
            self.draw_pieces()
            self.moves_shown = False
            self.curr_piece = None
            if self.board.mated(self.turn):
                self.after(2000, lambda: self.win('white' if self.turn == 'b' else 'black'))

