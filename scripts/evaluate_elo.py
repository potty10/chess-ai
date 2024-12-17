
import chess
import chess.pgn
import pexpect
from pexpect import popen_spawn
import itertools
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
from bots.stockfish_bot import StockfishBot
from bots.komodo_bot import KomodoBot

def evaluate_elo(results, bots):
    # https://stanislav-stankovic.medium.com/elo-rating-system-6196cc59941e
    c = 400
    k = 32

    results = zip(results["white"], results["black"], results["score"])
    bot_names = [bot.name for bot in bots]
    bot_elos = {name: 700 for name in bot_names}
    for result in results:
        white, black, score = result
        ra = bot_elos[white]
        rb = bot_elos[black]
        qa = 10**(ra/c)
        qb = 10**(rb/c)
        ea = qa / (qa + qb)
        eb = qb / (qa + qb)
        if score == "1/2-1/2":
            bot_elos[white] = int(ra + k * (0.5 - ea))
            bot_elos[black] = int(rb + k * (0.5 - eb))
        elif score == "1-0":
            bot_elos[white] = int(ra + k * (1 - ea))
            bot_elos[black] = int(rb + k * (0 - eb))
        elif score == "0-1":
            bot_elos[white] = int(ra + k * (0 - ea))
            bot_elos[black] = int(rb + k * (1 - eb))

    return bot_elos


def generate_stockfish_sample_matches(bots, no_games, filename, score_filename, elo_filename):
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
    bot_elos = evaluate_elo(result_csv, bots)
    bot_elos = pd.DataFrame(bot_elos.items(), columns=['name', 'elo'])
    bot_elos.to_csv(elo_filename, index=False)
    print(bot_elos)


if __name__ == "__main__":

    bots = [StockfishBot(f"Stockfish-{i}", i, "engines/stockfish-windows-x86-64-avx2.exe") for i in range(1, 6)]

    generate_stockfish_sample_matches(bots, 2, "output/history.pgn", "output/results.csv", "output/elo.csv")