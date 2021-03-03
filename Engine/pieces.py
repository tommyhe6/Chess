ROWS = 8
COLS = 8

def in_range(pos):
    return 0 <= pos[0] < ROWS and 0 <= pos[1] < COLS

def other(color):
    return 'w' if color == 'b' else 'b'


class Piece:
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.pos_pieces = board.pos_pieces

    def show_moves(self, straight, diagonal, dist, pos):
        moves = []
        d_orth = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        d_diag = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        if straight and diagonal:
            directions = d_orth + d_diag
        elif straight:
            directions = d_orth
        elif diagonal:
            directions = d_diag

        for d in directions:
            hit_piece = False
            for i in range(1, dist + 1):
                new_pos = (pos[0] + d[0] * i, pos[1] + d[1] * i)
                if in_range(new_pos) and new_pos not in self.pos_pieces[self.color] and not hit_piece:
                    moves.append(new_pos)
                else:
                    break
                if new_pos in self.pos_pieces[other(self.color)]:
                    hit_piece = True

        return moves

    def __repr__(self):
        return "repr_temp"

class Pawn(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.has_moved = False
        self.jump = -1

    def show_moves(self, pos):
        moves = []
        if self.color == 'w':
            dy = -1
        else:
            dy = 1
        diag = [(pos[0] + 1, pos[1] + dy), (pos[0] - 1, pos[1] + dy)]
        forward = [(pos[0], pos[1] + dy)]
        if not self.has_moved:
           if forward[0] not in self.board.pos_pieces[other(self.color)] and forward[0] not in self.board.pos_pieces[self.color]:
               forward.append((pos[0], pos[1] + 2*dy))
        for i in diag:
            if i in self.pos_pieces[other(self.color)]:
                moves.append(i)
        for i in forward:
            if i not in self.pos_pieces[self.color] and i not in self.pos_pieces[other(self.color)]:
                moves.append(i)
        moves += self.board.en_passant(pos)
        return moves

    def __repr__(self):
        return '{}p'.format(self.color)


class Knight(Piece):
    def show_moves(self, pos):
        moves = []
        dx = [-2, 2, -2, 2, -1, 1, -1, 1]
        dy = [1, -1, -1, 1, 2, -2, -2, 2]
        for i in range(8):
            new_pos = (pos[0] + dx[i], pos[1] + dy[i])
            if in_range(new_pos) and new_pos not in self.pos_pieces[self.color]:
                moves.append(new_pos)
        return moves

    def __repr__(self):
        return '{}n'.format(self.color)


class Rook(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.has_moved = False

    def show_moves(self, pos):
        return super().show_moves(True, False, 8, pos)

    def __repr__(self):
        return '{}r'.format(self.color)


class Bishop(Piece):
    def show_moves(self, pos):
        return super().show_moves(False, True, 8, pos)

    def __repr__(self):
        return '{}b'.format(self.color)


class Queen(Piece):
    def show_moves(self, pos):
        return super().show_moves(True, True, 8, pos)

    def __repr__(self):
        return '{}q'.format(self.color)


class King(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.has_moved = False

    def show_moves(self, pos):
        moves = super().show_moves(True, True, 1, pos)
        moves += self.board.castle(self.color)
        return moves

    def __repr__(self):
        return '{}k'.format(self.color)



