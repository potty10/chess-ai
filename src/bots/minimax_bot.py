import chess
import chess.polyglot
import sys
import os
from typing import Callable

sys.path.append(os.path.dirname(__file__))
from heuristics import *

WIN_VALUE = 9999999
DRAW_VALUE = 0

class MiniMaxAgent:

    def __init__(self, name, depth=2, ab_pruning=True):
        self.name = name
        self.depth = depth
        self.eval_func = larry_kaufman_piece_sum
        self.ab_pruning = ab_pruning

    def minimax_simple(self, board, maximizing_player, depth=2):
        '''
        Naive implementation of Minimax, for testing purposes
        '''
        def _minimax(depth, board, is_maximizing_node):

            outcome = board.outcome()
            if outcome:
                if outcome.winner == None:
                    return None, DRAW_VALUE
                if outcome.winner == maximizing_player:
                    return None, WIN_VALUE
                else:
                    return None, -WIN_VALUE

            if(depth == 0):
                return None, self.eval_func(board, maximizing_player)

            if(is_maximizing_node):
                bestMoveValue = float("-inf")
                bestMove = None
                nextMove = None
                for x in board.legal_moves:
                    move = chess.Move.from_uci(str(x))
                    board.push(move)
                    _, current_value = _minimax(depth - 1, board, not is_maximizing_node)
                    board.pop()
                    if current_value > bestMoveValue:
                        bestMove = move
                        bestMoveValue = current_value
                return bestMove, bestMoveValue
            else:
                bestMoveValue = float("inf")
                bestMove = None
                nextMove = None
                for x in board.legal_moves:
                    move = chess.Move.from_uci(str(x))
                    board.push(move)
                    _, current_value = _minimax(depth - 1, board, not is_maximizing_node)
                    board.pop()
                    if current_value < bestMoveValue:
                        bestMove = move
                        bestMoveValue = current_value

                return bestMove, bestMoveValue

        bestMove, _ = _minimax(depth, board, True)

        return bestMove

    def minimax_alpha_beta(self, board: chess.Board, eval_func: Callable, maximizing_player, depth=2):

        def _minimax(depth, board: chess.Board, is_maximizing_node: bool, alpha, beta):

            outcome = board.outcome()
            if outcome:
                if outcome.winner == None:
                    return None, DRAW_VALUE
                if outcome.winner == maximizing_player:
                    return None, WIN_VALUE
                else:
                    return None, -WIN_VALUE

            if(depth == 0):
                return None, eval_func(board, maximizing_player)

            if(is_maximizing_node):
                bestMoveValue = float('-inf')
                bestMove = None
                for x in board.legal_moves:
                    move = chess.Move.from_uci(str(x))
                    board.push(move)
                    _, current_value = _minimax(depth - 1, board, not is_maximizing_node, alpha, beta)
                    board.pop()

                    if current_value > bestMoveValue:
                        bestMove = move
                        bestMoveValue = current_value
                    
                    if bestMoveValue > beta:
                        return bestMove, bestMoveValue
                    alpha = max(alpha, bestMoveValue)

                return bestMove, bestMoveValue

            else:
                bestMoveValue = float('inf')
                bestMove = None
                for x in board.legal_moves:
                    move = chess.Move.from_uci(str(x))
                    board.push(move)
                    _, current_value = _minimax(depth - 1, board, not is_maximizing_node, alpha, beta)
                    board.pop()

                    if current_value < bestMoveValue:
                        bestMove = move
                        bestMoveValue = current_value

                    if bestMoveValue < alpha:
                        return bestMove, bestMoveValue
                    beta = min(beta, bestMoveValue)

                return bestMove, bestMoveValue

        bestMove, _ = _minimax(depth, board, True, float('-inf'), float('inf'))

        return bestMove
    
    def make_move(self, board: chess.Board):
        if self.ab_pruning:
            return self.minimax_alpha_beta(board, self.eval_func, board.turn, self.depth)
        else:  
            return self.minimax_simple(board, board.turn, self.depth)   