import chess
import random
from heuristics import *
from minimax import *
from engines.stockfish_bot import StockfishBot
import time

def random_choice(board):
    move = random.choice(list(board.legal_moves))
    return chess.Move.from_uci(str(move))


def get_statistics(no_games):
    '''
    Play the game n times and record statistics
    '''
    results = {
        "random_wins": 0,
        "minimax_wins": 0,
        "draws-stalemate": 0,
        "draws-insufficient_material": 0
    }

    termination_enums = {
        chess.Termination.CHECKMATE: "CHECKMATE",
        chess.Termination.STALEMATE: "STALEMATE",
        chess.Termination.INSUFFICIENT_MATERIAL: "INSUFFICIENT_MATERIAL",
        chess.Termination.SEVENTYFIVE_MOVES: "SEVENTYFIVE_MOVES",
        chess.Termination.FIVEFOLD_REPETITION: "FIVEFOLD_REPETITION",
        chess.Termination.FIFTY_MOVES: "FIFTY_MOVES",
        chess.Termination.THREEFOLD_REPETITION: "THREEFOLD_REPETITION"
    }
    win_count = [0,0] #white, black

    results = {i: 0 for i in range(1, 8)}

    # stockfish_bot = StockfishBot()
    for test_case in range(no_games):
        board = chess.Board()
        ttagent = MiniMaxAgent()
        # stockfish_bot.reset()
        n = 0
        moves = []
        decision_time = [0, 0]
        while True:
            if n%2 == 0: #White player
                start = time.time()
                move = ttagent.negamax(board, larry_kaufman_piece_sum, chess.WHITE, depth=3)  
                end = time.time()
                decision_time[0] += end - start
                # move = random_choice(board)
                #move = stockfish_bot.make_move(board)
                # move = minimax_alpha_beta_general(board, piece_count, chess.BLACK, depth=3)
                moves.append(move)
                board.push(move)
            else:
                # move = random_choice(board)
                start = time.time()
                move = negamax(board, larry_kaufman_piece_sum, chess.BLACK, depth=3)  
                end = time.time()  
                decision_time[0] += end - start 
                moves.append(move)
                board.push(move)

            n += 1
            outcome = board.outcome()
            if outcome:
                results[outcome.termination.value] += 1
                if outcome.termination == chess.Termination.CHECKMATE:
                    winner_idx = 0 if outcome.winner else 1
                    win_count[winner_idx] += 1

                # Record the history of moves
                with open("history.txt", "a") as f:
                    f.write(f'[Game {test_case}]\n')
                    f.write(f'[{str(outcome)}]\n')
                    move_history_str: str = chess.Board().variation_san(moves)
                    f.write(move_history_str)
                    f.write("\n")

                break

    result = {termination_enums[chess.Termination(i)]: results[i] for i in range(1, 8)}
    result["White Win"] = win_count[0]
    result["Black Win"] = win_count[1]
    result["White Time"] = decision_time[0]
    result["Black Time"] = decision_time[1]

    return result
            
if __name__ == "__main__":
    results = get_statistics(1)
    print(results)