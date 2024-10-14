from stockfish_bot import StockfishBot
from komodo_bot import KomodoBot
import chess
import chess.pgn
import pexpect
from pexpect import popen_spawn

def generate_stockfish_sample_matches(no_bots, no_games, filename):
    '''
    Play the game n times and record statistics
    '''
    open(filename, 'w').close()
    bots = [StockfishBot(f"Stockfish-{i*3}", i*3) for i in range(1, 1+no_bots)] + [StockfishBot(f"Komodo-{i*3}", i*3) for i in range(1, 1+no_bots)]

    for i, bot_white in enumerate(bots):
        for j, bot_black in enumerate(bots):
            if i == j:
                continue

            for _ in range(no_games):
                board = chess.Board()
                n = 0
                moves = []
                while True:
                    if n%2 == 0: #White player
                        move = bot_white.make_move(board)
                        moves.append(move)
                        board.push(move)
                    else:
                        move = bot_black.make_move(board)
                        moves.append(move)
                        board.push(move)

                    n += 1
                    outcome = board.outcome()
                    if outcome:
                        game = chess.pgn.Game().from_board(board)
                        game.headers["White"] = bot_white.name
                        game.headers["Black"] = bot_black.name
                        # Record the history of moves
                        with open(filename, "a+") as f:
                            f.write(str(game))
                            f.write("\n\n")
                        break

def parse_bayeselo_output(output: str):
    '''
    Parse the output of the Bayeselo program, which is the estimated elo of all
    players given a record of the games.
    '''
    lines = output.splitlines()[1:]
    result = []
    for line in lines:
        tokens = list(filter(None, line.split(" ")))
        result.append((tokens[0], tokens[1]))
    return result


def evaluate_elo(filename: str):
    child = popen_spawn.PopenSpawn("bayeselo.exe")
    child.expect(">")
    child.sendline("readpgn {}\n".format(filename))
    child.expect(">")
    child.sendline("elo")
    child.expect(">")
    child.sendline("mm")
    child.expect(">")
    child.sendline("ratings")
    child.expect ('>')
    child.sendline("ratings >rankings.txt")
    child.expect ('>')


if __name__ == "__main__":
    generate_stockfish_sample_matches(3,1, "history.pgn")
    evaluate_elo("history.pgn")