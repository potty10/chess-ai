from stockfish import Stockfish
import chess

class StockfishBot:

    empty_fen = chess.Board().fen()

    def __init__(self, name, depth):
        '''
        depth - int: Ranges from 1 to 20
        '''
        self.name = name
        self.stockfish_bot = Stockfish(path="./stockfish-windows-x86-64-avx2.exe", depth=depth)
    
    def reset(self):
        self.stockfish_bot.set_fen_position(self.empty_fen)

    def update_opponent_move(self, move):
        '''
        Update the bot with the latest move. I am not sure if it takes into
        account the fivefold rule.
        '''
        self.stockfish_bot.make_moves_from_current_position([str(move)])

    def make_move(self, board: chess.Board):
        '''
        Update stockfish with the latest board representation using FEN.
        FEN does not store the fivefold reptition rule, so I do not think it is 
        possible for stockfish to take into account the fivefold rule.
        '''
        fen_string = board.fen()
        self.stockfish_bot.set_fen_position(fen_string)
        return chess.Move.from_uci(self.stockfish_bot.get_best_move())