import Engine.utils
import chess
import random
import time
import math

def eval(board, color):
    val = 0
    for pos, piece in board.piece_map().items():
        r = pos // 8
        c = pos % 8
        if piece.symbol().isupper():
            val += Engine.utils.val_piece[piece.symbol().lower()] + Engine.utils.val_pos[piece.symbol().lower()][7 - r][c]
        else:
            val -= Engine.utils.val_piece[piece.symbol()] + Engine.utils.val_pos[piece.symbol()][r][c]
    return val if color == 'w' else -val

def minimax_AB(depth, board, maxi, color, alpha=-math.inf, beta=math.inf):
    if depth == 0:
        return (eval(board, color), None)
    best_val = -math.inf if maxi else math.inf
    best_move = None
    for mv in list(board.legal_moves):
        board.push(mv)
        cur_val = minimax_AB(depth - 1, board, not maxi, color, alpha, beta)[0]
        if maxi:
            if cur_val > best_val:
                best_val = cur_val
                best_move = mv
            alpha = max(alpha, cur_val)
        else:
            if cur_val < best_val:
                best_val = cur_val
                best_move = mv
            beta = min(beta, cur_val)
        board.pop()
        if beta <= alpha:
            break
    return (best_val, best_move)

def convert_board(board):
    pass
# return pos_pieces

def uci_to_mv(move):
    mv = move.uci()
    return ((ord(mv[0]) - ord('a'), 7 - ord(mv[1]) + ord('1')), (ord(mv[2]) - ord('a'), 7 - ord(mv[3]) + ord('1')))
# return as pair of pos

def mv_to_uci(move):
    return chess.Move.from_uci(f"{chr(ord('a') + move[0][0])}{chr(ord('8') - move[0][1])}{chr(ord('a') + move[1][0])}{chr(ord('8') - move[1][1])}")


if __name__ == "__main__":
#     board = chess.Board()
#     turns = 12
#     color = 'w'
#     t = time.time()
#     for i in range(turns):
#         (best_val, best_move) = minimax_AB(3, board, True, color)
#         print(best_val, convert_mv(best_move))
#         board.push(best_move)
#         print(board)
#         color = 'b' if color == 'w' else 'w'
#     print(f"TIME: {time.time() - t}")

    move = ((0, 0), (5, 4))
    print(mv_to_uci(move))

        
