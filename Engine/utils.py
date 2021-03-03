import chess

val_piece = {
    'p' : 100,
    'n' : 320,
    'b' : 330,
    'r' : 500,
    'q' : 900,
    'k' : 20000 
}

#Piece-Square Table

val_pos = {
    'p' : [
    [0,  0,  0,  0,  0,  0,  0,  0, ],
    [50, 50, 50, 50, 50, 50, 50, 50, ],
    [10, 10, 20, 35, 35, 20, 10, 10, ],
    [5,  5, 10, 30, 30, 10,  5,  5, ],
    [0,  0,  0, 25, 25,  0,  0,  0, ],
    [5, -5,-10,  0,  0,-10, -5,  5, ],
    [5, 10, 10,-30,-30, 10, 10,  5, ],
    [0,  0,  0,  0,  0,  0,  0,  0 ]],

    'n' : [
    [-50,-40,-30,-30,-30,-30,-40,-50, ],
    [-40,-20,  0,  0,  0,  0,-20,-40, ],
    [-30,  0, 10, 15, 15, 10,  0,-30, ],
    [-30,  5, 15, 20, 20, 15,  5,-30, ],
    [-30,  0, 15, 20, 20, 15,  0,-30, ],
    [-30,  5, 10, 15, 15, 10,  5,-30, ],
    [-40,-20,  0,  5,  5,  0,-20,-40, ],
    [-50,-40,-30,-30,-30,-30,-40,-50, ]],

    'b' : [
    [-20,-10,-10,-10,-10,-10,-10,-20, ],
    [-10,  0,  0,  0,  0,  0,  0,-10, ],
    [-10,  0,  5, 10, 10,  5,  0,-10, ],
    [-10,  5,  5, 10, 10,  5,  5,-10, ],
    [-10,  0, 10, 10, 10, 10,  0,-10, ],
    [-10, 10, 10, 10, 10, 10, 10,-10, ],
    [-10,  5,  0,  0,  0,  0,  5,-10, ],
    [-20,-10,-10,-10,-10,-10,-10,-20, ]],

    'r' : [
    [0,  0,  0,  0,  0,  0,  0,  0, ],
    [5, 10, 10, 10, 10, 10, 10,  5, ],
    [-5,  0,  0,  0,  0,  0,  0, -5, ],
    [-5,  0,  0,  0,  0,  0,  0, -5, ],
    [-5,  0,  0,  0,  0,  0,  0, -5, ],
    [-5,  0,  0,  0,  0,  0,  0, -5, ],
    [-5,  0,  0,  0,  0,  0,  0, -5, ],
    [0,  0,  0,  5,  5,  0,  0,  0 ]],

    'q' : [
    [-20,-10,-10, -5, -5,-10,-10,-20, ],
    [-10,  0,  0,  0,  0,  0,  0,-10, ],
    [-10,  0,  5,  5,  5,  5,  0,-10, ],
    [-5,  0,  5,  5,  5,  5,  0, -5, ],
    [0,  0,  5,  5,  5,  5,  0, -5, ],
    [-10,  5,  5,  5,  5,  5,  0,-10, ],
    [-10,  0,  5,  0,  0,  0,  0,-10, ],
    [-20,-10,-10, -5, -5,-10,-10,-20 ]],

    'k' : [
    # mid game
    [-30,-40,-40,-50,-50,-40,-40,-30, ],
    [-30,-40,-40,-50,-50,-40,-40,-30, ],
    [-30,-40,-40,-50,-50,-40,-40,-30, ],
    [-30,-40,-40,-50,-50,-40,-40,-30, ],
    [-20,-30,-30,-40,-40,-30,-30,-20, ],
    [-10,-20,-20,-20,-20,-20,-20,-10, ],
    [20, 20,  0,  0,  0,  0, 20, 20, ],
    [20, 30, 10,  0,  0, 10, 30, 20 ]]

    #end game
    # -50,-40,-30,-20,-20,-30,-40,-50,
    # -30,-20,-10,  0,  0,-10,-20,-30,
    # -30,-10, 20, 30, 30, 20,-10,-30,
    # -30,-10, 30, 40, 40, 30,-10,-30,
    # -30,-10, 30, 40, 40, 30,-10,-30,
    # -30,-10, 20, 30, 30, 20,-10,-30,
    # -30,-30,  0,  0,  0,  0,-30,-30,
    # -50,-30,-30,-30,-30,-30,-30,-50
}

def convert(board):
    board.pos_pieces
