from dataclasses import dataclass

class TicTacToe:

    # Enums
    DIRECTIONS = [(0,1), (1,0), (-1,1), (1,1)]
    PLAYER1, PLAYER2 = True, False

    def __init__(self, height = 3, width = 3, win_size = 3):

        if height <= 0 or width <= 0 or win_size <= 0:
            raise ValueError("Height, width and length of winning size must be postive integers")

        self.height = height
        self.width = width
        self.win_size = win_size

        # '-' for Empty, 'x' for player 1, 'o' for player 2
        self.board = [['-' for _ in range(width)] for _ in range(height)]
        self.turn = True
        self.move_history = []
        self.game_ended = False
        self.winner = None

    def __str__(self):
        '''
        Player 1 is represented by a 'x', player 2 is represented by a 'o'
        '''
        result = ''
        for r in self.board:
            result += ''.join(r)
            result += '\n'
        return result[:-1]

    def legal_moves(self):

        if self.game_ended:
            return

        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == '-':
                    yield (r, c)

    def legal_moves_random(self, size):
        pass

    def push(self, move):

        if self.game_ended:
            raise Exception("Game has ended")

        if self.board[move[0]][move[1]] != '-':
            raise ValueError("Illegal Move")

        cp = 'x' if self.turn else 'o'
        self.board[move[0]][move[1]] = cp
        self.move_history.append(move)
        
        # Check win
        for d in TicTacToe.DIRECTIONS:

            start_y = min(self.height - 1, max(0, move[0] - d[0] * self.win_size))
            start_x = min(self.width - 1, max(0, move[1] - d[1] * self.win_size))
            end_y = min(self.height - 1, max(0, move[0] + d[0] * self.win_size))
            end_x = min(self.width - 1, max(0, move[1] + d[1] * self.win_size))

            cnt = 0
            max_length = max(abs(end_y - start_y), abs(end_x - end_y)) + 1
            cur_y, cur_x = start_y,  start_x

            for i in range(max_length):
                if self.board[cur_y][cur_x] == cp:
                    cnt += 1
                    if cnt == self.win_size:
                        self.game_ended = True
                        self.winner = self.turn
                        break
                else:
                    cnt = 0
                cur_y += d[0]
                cur_x += d[1] 

        self.turn = not self.turn

    def pop(self):
        if self.game_ended:
            self.game_ended = False
            self.winner = None

        last_move = self.move_history.pop()
        self.board[last_move[0]][last_move[1]] = '-'
        self.turn = not self.turn
        return last_move

    def outcome(self):
        if self.game_ended:
            return self.winner
        return None

def test1():
    game = TicTacToe(3,3,3)
    assert game.outcome() == None
    game.push((1,1))
    assert game.outcome() == None
    try:
        game.push((1,1))
        assert False
    except:
        assert True
    game.push((0, 0))
    game.push((2,2))
    assert game.outcome() == None
    game.push((0,2))
    game.push((2, 0))
    game.push((0, 1))
    print(game.outcome())
    assert game.outcome() == TicTacToe.PLAYER2

if __name__ == '__main__':
    test1()