
'''
Evaluate ELO by benchmarking against stockfish with different elo
'''
import chess
import chess.pgn
import itertools
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
from bots.stockfish_bot import StockfishBot
from bots.komodo_bot import KomodoBot
from bots.minimax_bot_cpp import MinimaxBot
from bots.negamax_bot import NegaMaxAgent
from bots.minimax_bot import MiniMaxAgent

def mate_in_1_test(bot):
    print(f"mate_in_1_test: {bot.name}")
    test_fens = [
        "7B/8/8/8/8/8/pr6/k3K2R w K - 0 1", # Solution is O-O
        # "6k1/5ppp/p7/P7/5b2/7P/1r3PP1/3R2K1 w - - 0 1",
        # "r1bqkb1r/pppp1ppp/2n2n2/3Q4/2B1P3/8/PB3PPP/RN2K1NR w KQkq - 0 1"
    ]

    for fen in test_fens:
        board = chess.Board(fen)
        current_color = board.turn
        move = bot.make_move(board)
        board.push(move)
        if not board.outcome():
            print("Mate in 1 test failed: Game has not ended")
        elif board.outcome().termination != chess.Termination.CHECKMATE:
            print("Mate in 1 test failed: Game has not ended in checkmate")
        elif board.outcome().winner != current_color:
            print("Mate in 1 test failed: Winner is not the current player")
        else:
            print("Mate in 1 test passed")     

def mate_in_2_test(bot):
    print(f"mate_in_2_test: {bot.name}")
    test_fens = [
        "kbK5/pp6/1P6/8/8/8/8/R7 w - - 0 1",
        # "8/8/8/2P3R1/5B2/2rP1p2/p1P1PP2/RnQ1K2k w Q - 5 3"
    ]

    for fen in test_fens:
        board = chess.Board(fen)
        current_color = board.turn
        move = bot.make_move(board)
        board.push(move)
        print(move)
        board_copy = board.copy()
        print('-' * 50)
        for m in board.legal_moves:
            board = board_copy.copy()
            print(m)
            board.push(m)
            
            move = bot.make_move(board)
            print(move)
            print('-' * 50)
            board.push(move)
            if not board.outcome():
                print("Mate in 2 test failed: Game has not ended")
                break
            elif board.outcome().termination != chess.Termination.CHECKMATE:
                print("Mate in 2 test failed: Game has not ended in checkmate")
                break
            elif board.outcome().winner != current_color:
                print("Mate in 2 test failed: Winner is not the current player")
                break
            else:
                print("Mate in 2 test passed")     
    
if __name__ == "__main__":

    # Bots to test
    bots = []
    bots += [MiniMaxAgent("MiniMaxAB", depth=3)]
    bots += [MiniMaxAgent("MiniMax", ab_pruning=False, depth=3)]
    # bots += [NegaMaxAgent("NegaMaxTT", depth=3)]
    # bots += [NegaMaxAgent("NegaMax", use_transposition_table=False, depth=3)]

    
    for bot in bots:
        # try:
        mate_in_1_test(bot)
        # except Exception as e:
        #     print(e)
        # try:
        # mate_in_2_test(bot)
        # except Exception as e:
        #     print(e)