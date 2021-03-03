import Engine.pieces as pc
import copy

ROWS = 8
COLS = 8
SQUARE_SIZE = 64
WIDTH = ROWS * SQUARE_SIZE
HEIGHT = COLS * SQUARE_SIZE

def in_range(pos):
    return 0 <= pos[0] < ROWS and 0 <= pos[1] < COLS

def other(color):
    return 'w' if color=='b' else 'b'

#TODO actually properly determine draws rather than be lazy

class Board:
    def __init__(self):
        self.pos_pieces = {}
        self.pos_pieces['b'] = {
            (0, 0): pc.Rook('b', self),
            (1, 0): pc.Knight('b', self),
            (2, 0): pc.Bishop('b', self),
            (3, 0): pc.Queen('b', self),
            (4, 0): pc.King('b', self),
            (5, 0): pc.Bishop('b', self),
            (6, 0): pc.Knight('b', self),
            (7, 0): pc.Rook('b', self)
        }
        self.pos_pieces['w'] = {}
        for i in range(8):
            self.pos_pieces['b'][i, 1] = pc.Pawn('b', self)
        for pos, piece in self.pos_pieces['b'].items():
            new_pos = (pos[0], 7 - pos[1])
            self.pos_pieces['w'][new_pos] = type(piece)('w', self)
        self.move_number = 0

    def get_piece(self, pos):
        if pos in self.pos_pieces['w']:
            return self.pos_pieces['w'][pos]
        elif pos in self.pos_pieces['b']:
            return self.pos_pieces['b'][pos]
        else:
            return None
    
    def all_moves(self, color, exclude=type(None)):
        res = set()
        for pos, piece in self.pos_pieces[color].items():
            if not isinstance(piece, exclude):
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

    def move(self, pos1, pos2, new_piece=pc.Queen):
        piece = self.get_piece(pos1)
        if piece != None and pos2 in piece.show_moves(pos1):
            self.move_number += 1
            del self.pos_pieces[piece.color][pos1]
            if piece.color == 'b' and isinstance(piece, pc.Pawn) and pos2[1] == 7:
                self.pos_pieces[piece.color][pos2] = new_piece(piece.color, self)
            elif piece.color == 'w' and isinstance(piece, pc.Pawn) and pos2[1] == 0:
                self.pos_pieces[piece.color][pos2] = new_piece(piece.color, self)
            else:
                self.pos_pieces[piece.color][pos2] = piece
            check_moved = [pc.Pawn, pc.Rook, pc.King]
            for p in check_moved:
                if isinstance(piece, p):
                    piece.has_moved = True
            if isinstance(piece, pc.Pawn):
                if abs(pos1[0] - pos2[0]) == 1 and abs(pos1[1] - pos2[1]) == 1:
                    if pos2 not in self.pos_pieces[other(piece.color)]:
                        del self.pos_pieces[other(piece.color)][(pos2[0], pos1[1])]
                if abs(pos1[1] - pos2[1]) == 2:
                    piece.jump = self.move_number
            if pos2 in self.pos_pieces[other(piece.color)]:
                del self.pos_pieces[other(piece.color)][pos2]
            if isinstance(piece, pc.King):
                if pos2[0] - pos1[0] == 2:
                    self.pos_pieces[piece.color][(5, pos1[1])] = self.pos_pieces[piece.color][(7, pos1[1])]
                    del self.pos_pieces[piece.color][(7, pos1[1])]
                elif pos1[0] - pos2[0] == 2:
                    self.pos_pieces[piece.color][(3, pos1[1])] = self.pos_pieces[piece.color][(0, pos1[1])]
                    del self.pos_pieces[piece.color][(0, pos1[1])]


    def castle(self, color):
        res = []
        king_pos = [(4, 0)]
        rook = {}
        pos = {}
        rook['r'] = [(7, 0)]
        rook['l'] = [(0, 0)]
        pos['r'] = [(4, 0), (5, 0), (6, 0)]
        pos['l'] = [(4, 0), (3, 0), (2, 0), (1, 0)]
        if color == 'w':
            for i in [king_pos, rook['r'], rook['l'], pos['r'], pos['l']]:
                for j in range(len(i)):
                    i[j] = (i[j][0], 7 - i[j][1])

        for d in ['r', 'l']:
            if king_pos[0] in self.pos_pieces[color] and isinstance(self.pos_pieces[color][king_pos[0]], pc.King) and not self.pos_pieces[color][king_pos[0]].has_moved:
                if rook[d][0] in self.pos_pieces[color] and isinstance(self.pos_pieces[color][rook[d][0]], pc.Rook) and not self.pos_pieces[color][rook[d][0]].has_moved:
                    if [i not in self.all_moves(other(color), exclude=pc.King) for i in pos[d]] == [1, 1, 1, 1] if d == 'l' else [1, 1, 1]:
                        if [(i not in self.pos_pieces[color] and i not in self.pos_pieces[other(color)]) for i in pos[d][1:]] == ([1, 1, 1] if d == 'l' else [1, 1]):
                            res.append((king_pos[0][0] - 2 if d == 'l' else king_pos[0][0] + 2, king_pos[0][1]))
        return res

    def en_passant(self, pos):
        res = []
        curr_piece = self.get_piece(pos)
        if isinstance(curr_piece, pc.Pawn):
            sides = [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]
            for s in sides:
                if in_range(s) and s in self.pos_pieces[other(curr_piece.color)]:
                    side_piece = self.get_piece(s)
                    if isinstance(side_piece, pc.Pawn):
                        if self.move_number == side_piece.jump:
                            res.append((s[0], s[1] + (1 if curr_piece.color == 'b' else -1)))
        return res

    def mated(self, color):
        for pos, piece in self.pos_pieces[color].items():
            for m in piece.show_moves(pos):
                board_temp = copy.deepcopy(self)
                board_temp.move(pos, m)
                if not board_temp.in_check(color):
                    return False
        return True


