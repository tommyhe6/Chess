import pieces as pc
import copy

ROWS = 8
COLS = 8
SQUARE_SIZE = 64
WIDTH = ROWS * SQUARE_SIZE
HEIGHT = COLS * SQUARE_SIZE

def other(color):
    return 'w' if color=='b' else 'b'

#TODO determine when Draw

class Board:
    def __init__(self):
        self.pos_pieces = {}
        self.pos_pieces['w'] = {
            (0, 0): pc.Rook('w', self),
            (1, 0): pc.Knight('w', self),
            (2, 0): pc.Bishop('w', self),
            (3, 0): pc.King('w', self),
            (4, 0): pc.Queen('w', self),
            (5, 0): pc.Bishop('w', self),
            (6, 0): pc.Knight('w', self),
            (7, 0): pc.Rook('w', self)
        }
        self.pos_pieces['b'] = {}
        for i in range(8):
            self.pos_pieces['w'][i, 1] = pc.Pawn('w', self)
        for pos, piece in self.pos_pieces['w'].items():
            new_pos = (pos[0], 7 - pos[1])
            self.pos_pieces['b'][new_pos] = type(piece)('b', self)

    def get_piece(self, pos):
        if pos in self.pos_pieces['w']:
            return self.pos_pieces['w'][pos]
        elif pos in self.pos_pieces['b']:
            return self.pos_pieces['b'][pos]
        else:
            return None
    
    def all_moves(self, color):
        res = set()
        for pos, piece in self.pos_pieces[color].items():
            for i in piece.show_moves(pos):
                res.add(i)
        return res

    def get_king_pos(self, color):
        for pos, piece in self.pos_pieces[color].items():
            if isinstance(piece, pc.King):
                return pos

    def in_check(self, color):
        enemy_moves = self.all_moves(other(color))
        king_pos = self.get_king_pos(color)
        if king_pos in enemy_moves:
            return True
        return False

    def move(self, pos1, pos2, new_piece=None):
        piece = self.get_piece(pos1)
        if pos2 in piece.show_moves(pos1):
            del self.pos_pieces[piece.color][pos1]
            if isinstance(piece, pc.Pawn) and pos2[1] == 7:
                self.pos_pieces[piece.color][pos2] = new_piece
            else:
                if isinstance(piece, pc.Pawn):
                    piece.has_moved = True
                if pos2 in self.pos_pieces[other(piece.color)]:
                    del self.pos_pieces[other(piece.color)][pos2]
                self.pos_pieces[piece.color][pos2] = piece

    def mated(self, color):
        for pos, piece in self.pos_pieces[color].items():
            for m in piece.show_moves(pos):
                board_temp = copy.deepcopy(self)
                board_temp.move(pos, m)
                if not board_temp.in_check(color):
                    return False
        return True

    def draw(self):
        pass

# b = Board()
# p = b.pos_pieces['b'][1, 6]
# print(type(p))
# print(p.show_moves())

