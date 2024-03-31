from stockfish_bot import StockfishBot
from komodo_bot import KomodoBot
import chess
import chess.pgn
import subprocess

def generate_sample_matches(no_games, filename):
    '''
    Play the game n times and record statistics
    '''
    stockfish_bots = [StockfishBot(f"Stockfish-{i}", i) for i in range(1, 11)]

    for i, bot_white in enumerate(stockfish_bots):
        for j, bot_black in enumerate(stockfish_bots):
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
                            f.write("\n")
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
    p = subprocess.Popen(["bayeselo"], bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        print(line)
    print("Process opened")
    p.stdin.write(b'elo\n')
    p.stdin.flush()
    for line in iter(p.stdout.readline, b''):
        pass
    print("ELo command sent")
    p.stdin.write(b'mm\n')
    p.stdin.flush()
    for line in iter(p.stdout.readline, b''):
        pass
    print("mm command sent")
    p.stdin.write(b'ratings\n')
    p.stdin.flush()
    print("ratings command sent")
    for line in iter(p.stdout.readline, b''):
        print(line)
    print(stdout)
    player_and_elo = parse_bayeselo_output(stdout)
    print("Output parsed")
    with open("rankings.txt", "a+") as f:
        for player_name, elo in player_and_elo:
            f.write(f"{player_name},{elo}\n")

if __name__ == "__main__":
    # generate_sample_matches(3, "history.txt")
    evaluate_elo("rankings.txt")