import chess

def piece_count(board, is_maximising_player):
    '''
    Heuristic that is the sum of pieces.

    is_white: bool - indicates which player is the maximising player. If white is the 
    maximising player, the heuristic value is positive if white has a higher advantage.
    '''

    def getPieceValue(piece):
        if(piece == None):
            return 0
        value = 0
        if piece == "P" or piece == "p":
            value = 10
        if piece == "N" or piece == "n":
            value = 30
        if piece == "B" or piece == "b":
            value = 30
        if piece == "R" or piece == "r":
            value = 50
        if piece == "Q" or piece == "q":
            value = 90
        if piece == 'K' or piece == 'k':
            value = 900
        return value

    result = 0
    for i in range(64):
        if board.piece_at(i):
            if bool(board.piece_at(i).color):
                result += getPieceValue(str(board.piece_at(i)))
            else:
                result -= getPieceValue(str(board.piece_at(i)))
    
    if is_maximising_player:
        return result
    return -result

def larry_kaufman_piece_sum(board: chess.Board, maximising_player):
    '''
    Heuristic based on king safety and board position

    is_white: bool - indicates which player is the maximising player. If white is the 
    maximising player, the heuristic value is positive if white has a higher advantage.
    If black is the maximising player, the heuristic value is positive if black has a
    higher advantage.
    '''
    # https://www.chess.com/article/view/the-evaluation-of-material-imbalances-by-im-larry-kaufman
    piece_value = {
        "p": 100,
        "b": 325,
        "n": 325,
        "r": 500,
        "q": 975,
        "k": 0 # King has no value
    }

    result = 0
    bishop_count = [0, 0] # (white bishop, black bishop)

    for i in range(64):
        if board.piece_at(i):
            piece: str = str.lower(str(board.piece_at(i)))
            if bool(board.piece_at(i).color): # white
                result += piece_value[piece]
                if piece == 'b':
                    bishop_count[0] += 1
            else:
                result -= piece_value[piece]
                if piece == 'b':
                    bishop_count[1] += 1
    
    # Bishop bonus
    if bishop_count[0] == 2:
        result += 50
    if bishop_count[1] == 2:
        result -= 50
    
    if maximising_player == chess.WHITE:
        return result
    return -result

# Piece square table
# https://www.chessprogramming.org/Simplified_Evaluation_Function
PIECE_SQUARE_TABLE = {
    chess.BISHOP: (
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,
    ),
    chess.KING: (
        20, 30, 10,  0,  0, 10, 30, 20,
        20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
    ),
    chess.KNIGHT: (
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,
    ),
    chess.PAWN: (
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10,-20,-20, 10, 10,  5,
        5, -5,-10,  0,  0,-10, -5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0,  0,  0,  0,  0,  0,  0,  0,
    ),
    chess.QUEEN: (
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -10,  5,  5,  5,  5,  5,  0,-10,
        0,  0,  5,  5,  5,  5,  0, -5,
        -5,  0,  5,  5,  5,  5,  0, -5,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20,
    ),
    chess.ROOK: (
         0,  0,  0,  5,  5,  0,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         5, 10, 10, 10, 10, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0,
    ),
}

def piece_square_table_eval(board: chess.Board, maximising_player):
    result = 0
    for i in range(64):
        if board.piece_at(i):
            piece = board.piece_at(i).piece_type
            if board.piece_at(i).color == chess.WHITE:
                result += PIECE_SQUARE_TABLE[piece][i]
            else:
                result -= PIECE_SQUARE_TABLE[piece][63-i]
    if maximising_player == chess.WHITE:
        return result
    return -result

