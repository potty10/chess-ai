import chess

class KomodoBot:

    def __init__(self, name: str, depth, executable_path="./komodo-14.1-64bit.exe"):
        '''
        depth - int: Ranges from 
        '''
        self.name = name
        self.engine = chess.engine.SimpleEngine.popen_uci(executable_path)
        self.depth = depth

    def make_move(self, board: chess.Board):
        result = self.engine.play(board, chess.engine.Limit(depth = self.depth))
        return result.move