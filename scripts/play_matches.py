
'''
Evaluate ELO by benchmarking against stockfish with different elo
'''
import chess
import chess.pgn
import pexpect
from pexpect import popen_spawn
import itertools
import sys
import os
import pandas as pd
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
from bots.stockfish_bot import StockfishBot
from bots.komodo_bot import KomodoBot
from bots.minimax_bot_cpp import MinimaxBot
from bots.negamax_bot import NegaMaxAgent
from bots.minimax_bot import MiniMaxAgent
from bots.mcts_bot import MCTSAgent
from bots.mcts_bot import MCTSAgent as DMCTSAgent

def tally_score(results, bots):
    results = zip(results["white"], results["black"], results["score"])
    bot_names = [bot.name for bot in bots]
    bot_scores = {name: 0 for name in bot_names}

    for result in results:
        white, black, score = result
        if score == "1/2-1/2":
            bot_scores[white] += 0.5
            bot_scores[black] += 0.5
        elif score == "1-0":
            bot_scores[white] += 1
        elif score == "0-1":
            bot_scores[black] += 1

    return bot_scores

def generate_sample_matches(bots, no_games, filename, score_filename, elo_filename):
    '''
    Each bot plays against each other n times
    '''
    open(filename, 'w').close()
    result = {'white':[], 'black':[], 'score':[]}
    for bot_white, bot_black in itertools.combinations(bots, 2):
        for _ in range(no_games):
            board = chess.Board()
            n = 0
            while True:
                if n%2 == 0: #White player
                    move = bot_white.make_move(board)
                    board.push(move)
                else:
                    move = bot_black.make_move(board)
                    board.push(move)
                n += 1
                if board.outcome():
                    break

            game = chess.pgn.Game().from_board(board)
            game.headers["White"] = bot_white.name
            game.headers["Black"] = bot_black.name

            # Record the history of moves
            with open(filename, "a+") as f:
                f.write(str(game))
                f.write("\n\n")

            # Store results in Dataframe
            result['white'].append(bot_white.name)
            result['black'].append(bot_black.name)
            result['score'].append(str(board.outcome().result()))

    # Save results to CSV
    result_csv = pd.DataFrame(result)
    result_csv.to_csv(score_filename, index=False)

    # Evaluate ELO
    bot_scores = tally_score(result_csv, bots)
    bot_scores = pd.DataFrame(bot_scores.items(), columns=['name', 'scores'])
    bot_scores.to_csv(elo_filename, index=False)
    print(bot_scores)


if __name__ == "__main__":
    # Windows
    #bots = [StockfishBot(f"Stockfish-{i}", i, "engines/stockfish-windows-x86-64-avx2.exe") for i in range(1, 6)]

    # Linux
    bots = []
    # for i in range(5,10):
    #     bots.append(StockfishBot(f"Stockfish-{i*100}", 10, "engines/stockfish-ubuntu-x86-64-avx2",{"UCI_Elo": i*100}))

    # bots += [MinimaxBot("Mybot", "src/cpp/agent")]
    # bots += [NegaMaxAgent("NegaMax")]
    bots += [DMCTSAgent("Discount")]
    # bots += [StockfishBot(f"Stockfish", 5, "engines/stockfish-windows-x86-64-avx2.exe")]
    bots += [MCTSAgent("MCTS")]

    intermediate_path = os.path.join("output", f"play_matches-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")
    os.makedirs(intermediate_path, exist_ok=True)
    
    generate_sample_matches(bots, 
                            2, 
                            os.path.join(intermediate_path, "history.pgn"),
                            os.path.join(intermediate_path, "results.csv"),
                            os.path.join(intermediate_path, "scores.csv")
                            )