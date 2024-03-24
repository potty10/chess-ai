import chess
from heuristics import *
from typing import Callable

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
            bestMoveValue = float("-inf")
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = max(bestMoveValue,_minimax(depth - 1, board, not is_maximizing))
                board.pop()
            return bestMoveValue
        else:
            bestMoveValue = float("inf")
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

class MiniMaxAgent:

    transposition_table = {

    }

    def reset(self):
        self.transposition_table = {}




def minimax2(board: chess.Board, eval_func: Callable, isMaximizing=True, depth=2, limit=None):
    '''
    Perform the minimax algorithm with alpha beta pruning.
    Assumse that the game has not ended, and there are still valid moves.
    Works for both black and white.

    eval_func - Callable[[chess.Board, bool], int]: evaluation function that takes
    in chess.Board and the bool that evaluates to true if white is the maximising plater.

    limit - int: Instead of exploring all possible moves, explore only a random subset of 
    moves. If None, explore all moves.
    '''
    def _minimax(depth, board: chess.Board, is_maximizing: bool, alpha, beta):

        outcome = board.outcome()
        if outcome:
            if outcome.winner == chess.WHITE:
                return -9999999
            if outcome.winner == chess.BLACK:
                return 9999999

        if(depth == 0):
            return eval_func(board, is_maximizing)

        possibleMoves = board.legal_moves

        if(is_maximizing):
            bestMoveValue = float('-inf')
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
            bestMoveValue = float('inf')
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = min(bestMoveValue, _minimax(depth - 1, board, not is_maximizing, alpha, beta))
                board.pop()
                beta = min(beta,bestMoveValue)
                if(beta <= alpha):
                    return bestMoveValue
            return bestMoveValue

    bestMoveValue = float('-inf')
    bestMove = None

    # There is only 1 move, have to return it
    # if board.legal_moves.count() == 1:
    #     for x in board.legal_moves:
    #         return chess.Move.from_uci(str(x))

    for x in board.legal_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = _minimax(depth - 1, board, not isMaximizing, float('-inf'), float('inf'))
        board.pop()
        if( value > bestMoveValue):
            bestMoveValue = value
            bestMove = move
    return bestMove