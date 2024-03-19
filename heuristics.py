import chess

def piece_count(board, is_white=True):
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
    
    if is_white:
        return result
    return -result

def center_and_king(board: chess.Board, is_white=True):
    '''
    Heuristic based on king safety and board position

    is_white: bool - indicates which player is the maximising player. If white is the 
    maximising player, the heuristic value is positive if white has a higher advantage.
    '''
    result = 0

    for move in board.legal_moves:
        # Position is good if many pieces can attack the centre
        if move.to_square in (chess.D4, chess.D5, chess.E4, chess.E5):
            result += 200
        