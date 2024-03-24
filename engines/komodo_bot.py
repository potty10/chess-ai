import chess

class KomodoBot:

    def __init__(self, name: str, depth):
        '''
        depth - int: Ranges from 
        '''
        self.name = name
        self.engine = chess.engine.SimpleEngine.popen_uci("./komodo-14.1-64bit.exe")
        self.depth = depth

    def make_move(self, board: chess.Board):
        result = self.engine.play(board, chess.engine.Limit(depth = self.depth))
        return result.move