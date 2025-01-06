import chess
import chess.polyglot
import sys
import os
from typing import Callable
from enum import Enum
from collections import namedtuple

sys.path.append(os.path.dirname(__file__))
from heuristics import *

WIN_VALUE = 9999999
DRAW_VALUE = 0

class NegaMaxAgent:

    # Transposition table is key-value dirciontary. 
    # Key is state of board, value is tuple (flag, value, depth, move)
    class TTFlag(Enum):
        EXACT = 1
        UPPERBOUND = 2
        LOWERBOUND = 3

    TTEntry = namedtuple("TTEntry", ['flag', 'value', 'depth', 'move'])

    def __init__(self, name, depth=2, use_transposition_table=True):
        self.name = name
        self.depth = depth
        self.eval_func = larry_kaufman_piece_sum
        self.use_transposition_table = use_transposition_table

    transposition_table = {}

    def reset_transposition_table(self):
        self.transposition_table = {}

    def negamax_transposition_table(self, board: chess.Board, eval_func: Callable, player_color, depth=2):
        '''
        Run Negamax algorithm
        '''
        def _negamax(depth, board: chess.Board, color, alpha, beta):
            
            alpha_orignal = alpha

            tt_key = chess.polyglot.zobrist_hash(board)
            if tt_key in self.transposition_table and self.transposition_table[tt_key].depth >= depth:
                ttentry = self.transposition_table[tt_key]
                if ttentry.flag == NegaMaxAgent.TTFlag.EXACT:
                    return ttentry.move, ttentry.value
                elif ttentry.flag == NegaMaxAgent.TTFlag.LOWERBOUND:
                    alpha = max(alpha, ttentry.value)
                elif ttentry.flag == NegaMaxAgent.TTFlag.UPPERBOUND:
                    beta = min(beta, ttentry.value)         
                if alpha >= beta:
                    return ttentry.move, ttentry.value

            outcome = board.outcome()
            if outcome:
                if outcome.winner == None:
                    return None, DRAW_VALUE
                if outcome.winner == chess.WHITE:
                    return None, color * WIN_VALUE
                else:
                    return None, -WIN_VALUE * color

            if(depth == 0):
                return None, color * eval_func(board, chess.WHITE)

            bestMoveValue = float('-inf')
            bestMove = None
            for x in board.legal_moves:

                move = chess.Move.from_uci(str(x))
                board.push(move)
                _, current_value = _negamax(depth - 1, board, -color, -beta, -alpha)
                current_value = -current_value
                board.pop()

                if current_value > bestMoveValue:
                    bestMove = move
                    bestMoveValue = current_value
                
                if bestMoveValue > beta:
                    return bestMove, bestMoveValue
                alpha = max(alpha, bestMoveValue)

            newflag = NegaMaxAgent.TTFlag.EXACT
            if bestMoveValue <= alpha_orignal:
                newflag = NegaMaxAgent.TTFlag.UPPERBOUND
            elif bestMoveValue >= beta:
                newflag = NegaMaxAgent.TTFlag.LOWERBOUND
            new_tt_entry = NegaMaxAgent.TTEntry(value=bestMoveValue, move=bestMove, depth=depth, flag=newflag)

            self.transposition_table[tt_key] = new_tt_entry

            return bestMove, bestMoveValue

        color = 1 if player_color == chess.WHITE else -1
        bestMove, _ = _negamax(depth, board, color, float('-inf'), float('inf'))

        return bestMove
    
    def negamax(self, board: chess.Board, eval_func: Callable, player_color, depth=2):
        def _negamax(depth, board: chess.Board, color, alpha, beta):
            outcome = board.outcome()
            if outcome:
                if outcome.winner == None:
                    return None, DRAW_VALUE
                if outcome.winner == chess.WHITE:
                    return None, color * WIN_VALUE
                else:
                    return None, -WIN_VALUE * color

            if(depth == 0):
                return None, color * eval_func(board, chess.WHITE)

            bestMoveValue = float('-inf')
            bestMove = None
            for x in board.legal_moves:

                move = chess.Move.from_uci(str(x))
                board.push(move)
                _, current_value = _negamax(depth - 1, board, -color, -beta, -alpha)
                current_value = -current_value
                board.pop()

                if current_value > bestMoveValue:
                    bestMove = move
                    bestMoveValue = current_value
                
                if bestMoveValue > beta:
                    return bestMove, bestMoveValue
                alpha = max(alpha, bestMoveValue)

            return bestMove, bestMoveValue

        color = 1 if player_color == chess.WHITE else -1
        bestMove, _ = _negamax(depth, board, color, float('-inf'), float('inf'))

        return bestMove

    def make_move(self, board: chess.Board):
        if self.use_transposition_table:
            return self.negamax_transposition_table(board, self.eval_func, board.turn, self.depth)
        else:
            return self.negamax(board, self.eval_func, board.turn, self.depth)   