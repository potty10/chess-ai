import chess
import random
from heuristics import *
from minimax import *

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

    for test_case in range(no_games):
        board = chess.Board()
        n = 0
        moves = []
        while True:
            if n%2 == 0:
                move = random_choice(board)
                moves.append(move)
                board.push(move)
            else:
                move = minimax2(board)
                moves.append(move)
                board.push(move)

            n += 1
            outcome = board.outcome()
            if outcome:
                if board.is_stalemate():
                    results["draws-stalemate"] += 1
                
                # Neither side has sufficient winning material
                if board.is_insufficient_material():
                    results["draws-insufficient_material"] += 1

                if board.is_checkmate():
                    if outcome.winner == chess.WHITE:
                        results["random_wins"] += 1
                    else:
                        results["minimax_wins"] += 1

                # Record the history of moves
                with open("history.txt", "a") as f:
                    f.write(f'[Game {test_case}]\n')
                    f.write(f'[{str(outcome)}]\n')
                    move_history_str: str = chess.Board().variation_san(moves)
                    f.write(move_history_str)
                    f.write("\n")

                break

    return results
            
if __name__ == "__main__":
    results = get_statistics(10)
    print(results)