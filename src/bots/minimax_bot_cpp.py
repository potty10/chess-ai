import subprocess
from typing import Any, List, Optional
import copy
from os import path
from dataclasses import dataclass
from enum import Enum
import re
import chess

class StockfishException(Exception):
    pass


class MinimaxBot:
    """Integrates the Stockfish chess engine with Python."""

    _del_counter = 0
    # Used in test_models: will count how many times the del function is called.

    def __init__(
        self, name, path: str = "stockfish", depth: int = 15
    ) -> None:
        
        self.name = name

        self._path = path
        self._stockfish = subprocess.Popen(
            self._path,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self._has_quit_command_been_sent = False

        self.depth = str(depth)


    def _put(self, command: str) -> None:
        if not self._stockfish.stdin:
            raise BrokenPipeError()
        if self._stockfish.poll() is None and not self._has_quit_command_been_sent:
            self._stockfish.stdin.write(f"{command}\n")
            self._stockfish.stdin.flush()
            if command == "quit":
                self._has_quit_command_been_sent = True

    def _read_line(self) -> str:
        if not self._stockfish.stdout:
            raise BrokenPipeError()
        if self._stockfish.poll() is not None:
            raise StockfishException("The Stockfish process has crashed")
        return self._stockfish.stdout.readline().strip()


    def get_best_move(self, fen_position: str) -> Optional[str]:
        """Returns best move with current position on the board.
        wtime and btime arguments influence the search only if provided.

        Returns:
            A string of move in algebraic notation or None, if it's a mate now.
        """
        # if wtime is not None or btime is not None:
        #     self._go_remaining_time(wtime, btime)
        # else:
        self._put(f"depth {self.depth}")
        self._put(f"fen {fen_position}")
        best_move = self._read_line()
        return best_move

    def make_move(self, board: chess.Board):
        '''
        Update stockfish with the latest board representation using FEN.
        FEN does not store the fivefold reptition rule, so I do not think it is 
        possible for stockfish to take into account the fivefold rule.
        '''
        fen_string = board.fen()
        return chess.Move.from_uci(self.get_best_move(fen_string))
    