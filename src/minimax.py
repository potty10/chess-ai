import chess
import chess.polyglot
from heuristics import *
from typing import Callable
from enum import Enum
from collections import namedtuple

WIN_VALUE = 9999999
DRAW_VALUE = 0

def minimax_simple(board, maximizing_player, is_maximizing_node=True, depth=2):

    def _minimax(depth, board, is_maximizing_node):

        outcome = board.outcome()
        if outcome:
            if outcome.winner == None:
                return DRAW_VALUE
            if outcome.winner == maximizing_player:
                return WIN_VALUE
            else:
                return -WIN_VALUE

        if(depth == 0):
            return piece_count(board, maximizing_player)

        if(is_maximizing_node):
            bestMoveValue = float("-inf")
            for x in board.legal_moves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = max(bestMoveValue,_minimax(depth - 1, board, not is_maximizing_node))
                board.pop()
            return bestMoveValue
        else:
            bestMoveValue = float("inf")
            for x in board.legal_moves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = min(bestMoveValue, _minimax(depth - 1, board, not is_maximizing_node))
                board.pop()
            return bestMoveValue

    bestMoveValue = float("-inf")
    bestMove = None

    for x in board.legal_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = _minimax(depth - 1, board, not is_maximizing_node)
        board.pop()
        if( value > bestMoveValue):
            bestMoveValue = value
            bestMove = move
    return bestMove

def minimax_alpha_beta(board: chess.Board, eval_func: Callable, maximizing_player, depth=2):

    def _minimax(depth, board: chess.Board, is_maximizing_node: bool, alpha, beta):

        outcome = board.outcome()
        if outcome:
            if outcome.winner == None:
                return DRAW_VALUE
            if outcome.winner == maximizing_player:
                return WIN_VALUE
            else:
                return -WIN_VALUE

        if(depth == 0):
            return eval_func(board, maximizing_player)

        if(is_maximizing_node):
            bestMoveValue = float('-inf')
            for x in board.legal_moves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = max(bestMoveValue,_minimax(depth - 1, board, not is_maximizing_node, alpha, beta))
                board.pop()
                alpha = max(alpha, bestMoveValue)
                if beta < alpha:
                    return bestMoveValue
            return bestMoveValue
        else:
            bestMoveValue = float('inf')
            for x in board.legal_moves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMoveValue = min(bestMoveValue, _minimax(depth - 1, board, not is_maximizing_node, alpha, beta))
                board.pop()
                beta = min(beta,bestMoveValue)
                if beta < alpha:
                    return bestMoveValue
            return bestMoveValue

    bestMoveValue = float('-inf')
    bestMove = None

    for x in board.legal_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = _minimax(depth - 1, board, False, float('-inf'), float('inf'))
        board.pop()
        if( value > bestMoveValue):
            bestMoveValue = value
            bestMove = move
    return bestMove

def minimax_alpha_beta_general(board: chess.Board, eval_func: Callable, maximizing_player, depth=2):

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


def negamax(board: chess.Board, eval_func: Callable, player_color, depth=2):
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



class MiniMaxAgent:

    class TTFlag(Enum):
        EXACT = 1
        UPPERBOUND = 2
        LOWERBOUND = 3

    TTEntry = namedtuple("TTEntry", ['flag', 'value', 'depth', 'move'])

    transposition_table = {}

    def reset_transposition_table(self):
        self.transposition_table = {}

    def negamax(self, board: chess.Board, eval_func: Callable, player_color, depth=2):
        def _negamax(depth, board: chess.Board, color, alpha, beta):
            
            alpha_orignal = alpha

            tt_key = chess.polyglot.zobrist_hash(board)
            if tt_key in self.transposition_table and self.transposition_table[tt_key].depth >= depth:
                ttentry = self.transposition_table[tt_key]
                if ttentry.flag == MiniMaxAgent.TTFlag.EXACT:
                    return ttentry.move, ttentry.value
                elif ttentry.flag == MiniMaxAgent.TTFlag.LOWERBOUND:
                    alpha = max(alpha, ttentry.value)
                elif ttentry.flag == MiniMaxAgent.TTFlag.UPPERBOUND:
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

            newflag = MiniMaxAgent.TTFlag.EXACT
            if bestMoveValue <= alpha_orignal:
                newflag = MiniMaxAgent.TTFlag.UPPERBOUND
            elif bestMoveValue >= beta:
                newflag = MiniMaxAgent.TTFlag.LOWERBOUND
            new_tt_entry = MiniMaxAgent.TTEntry(value=bestMoveValue, move=bestMove, depth=depth, flag=newflag)

            self.transposition_table[tt_key] = new_tt_entry

            return bestMove, bestMoveValue

        color = 1 if player_color == chess.WHITE else -1
        bestMove, _ = _negamax(depth, board, color, float('-inf'), float('inf'))

        return bestMove
