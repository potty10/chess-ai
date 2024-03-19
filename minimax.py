import chess
from heuristics import *

def minimax(board, isMaximizing=True, depth=2):
    '''
    Perform the minimax algorithm without alpha beta pruning.
    Assumse that the game has not ended, and there are still valid moves.
    '''
    def _minimax(depth, board, is_maximizing):

        outcome = board.outcome()
        if outcome:
            if outcome.winner == chess.WHITE:
                return -99999
            if outcome.winner == chess.BLACK:
                return 99999

        if(depth == 0):
            return piece_count(board, False)

        possibleMoves = board.legal_moves

        if(is_maximizing):
            bestMoveValue = -9999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = max(bestMoveValue,_minimax(depth - 1, board, not is_maximizing))
                board.pop()
            return bestMoveValue
        else:
            bestMoveValue = 9999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = min(bestMoveValue, _minimax(depth - 1, board, not is_maximizing))
                board.pop()
            return bestMoveValue

    bestMoveValue = -9999
    bestMove = None

    for x in board.legal_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = _minimax(depth - 1, board, not isMaximizing)
        board.pop()
        if( value > bestMoveValue):
            bestMoveValue = value
            bestMove = move
    return bestMove


def minimax2(board, isMaximizing=True, depth=2):
    '''
    Perform the minimax algorithm with alpha beta pruning.
    Assumse that the game has not ended, and there are still valid moves.
    '''
    def _minimax(depth, board, is_maximizing, alpha, beta):

        outcome = board.outcome()
        if outcome:
            if outcome.winner == chess.WHITE:
                return -99999
            if outcome.winner == chess.BLACK:
                return 99999

        if(depth == 0):
            return piece_count(board, False)

        possibleMoves = board.legal_moves

        if(is_maximizing):
            bestMoveValue = -9999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = max(bestMoveValue,_minimax(depth - 1, board, not is_maximizing, alpha, beta))
                board.pop()
                alpha = max(alpha, bestMoveValue)
                if beta <= alpha:
                    return bestMoveValue
            return bestMoveValue
        else:
            bestMoveValue = 9999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = min(bestMoveValue, _minimax(depth - 1, board, not is_maximizing, alpha, beta))
                board.pop()
                beta = min(beta,bestMoveValue)
                if(beta <= alpha):
                    return bestMoveValue
            return bestMoveValue

    bestMoveValue = -9999
    bestMove = None

    for x in board.legal_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = _minimax(depth - 1, board, not isMaximizing, float('-inf'), float('inf'))
        board.pop()
        if( value > bestMoveValue):
            bestMoveValue = value
            bestMove = move
    return bestMove