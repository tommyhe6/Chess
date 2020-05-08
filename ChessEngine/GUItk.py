import tkinter as tk
from tkinter.font import Font
import os
from board import Board
import copy
from PIL import ImageTk, Image

ROWS = 8
COLS = 8
SQUARE_SIZE = 64
WIDTH = ROWS * SQUARE_SIZE
HEIGHT = COLS * SQUARE_SIZE

#TODO switching pawn piece

def other(color):
    return 'w' if color == 'b' else 'b'

def pos_to_pixel(pos, x, y):
    x[0] = pos[0] * SQUARE_SIZE
    x[1] = x[0] + SQUARE_SIZE
    y[0] = pos[1] * SQUARE_SIZE
    y[1] = y[0] + SQUARE_SIZE

class GUI(tk.Frame):
    def __init__(self, root, board):
        tk.Frame.__init__(self, root)
        self.root = root;
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(side='top', fill='both', expand='true')
        self.canvas.bind('<Button-1>', self.click)
        self.board = board
        self.moves_shown = False
        self.last = {}
        self.turn = 'w'
        self.prev_moves = []

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
                p = ImageTk.PhotoImage(Image.open('../Imgs/{}.png'.format(repr(piece))).convert('RGBA'))
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

    def move_piece(self, pos1, pos2):
        piece1 = self.get_piece(pos1)
        self.board.move(pos1, pos2)

    def click(self, event):
        pos = self.get_coords(event)
        piece = self.get_piece(pos)
        if not self.moves_shown:
            if piece is not None and piece.color == self.turn:
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
                board_temp.move(self.last['pos'], pos)
                if not board_temp.in_check(self.turn):
                    self.board = board_temp
                    self.turn = other(self.turn)
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
            if self.board.mated(self.turn):
                self.canvas.create_text(200, 200, font=Font(size=36), text='{} won!'.format('white' if self.turn == 'w' else 'black'))
            self.moves_shown = False
            self.curr_piece = None

