# Chess notation
`python-chess` uses these notations, so it will be good to understand them.

## Algebraic notation <sup>[^fn1]</sup><sup>[^fn2]</sup>
A game or series of moves is generally written in one of two ways; in two columns, as White/Black pairs, preceded by the move number and a period:
```
1. e4 e5
2. Nf3 Nc6
3. Bb5 a6
```
or horizontally:
```
1. e4 e5 2. Nf3 Nc6 3. Bb5 a6
```
A move is written as
```
castling := 0-0 | 0-0-0
pawn_move := [<file_letter>x]<to_square>[+|#]
move := <piece_name>[file_letter|rank_number][x]<dest_square>[+|#]
```

- Players use the letters K for king, Q for queen, R for rook, B for bishop, and N for knight. The pawn is the only piece that has no abbreviation. 

- When any piece is captured, a lower-case "x" is placed in between the piece and the square where the capture occurs. For example, `Bxe5` (bishop captures the piece on e5)

- When a pawn captures a piece, you write the name of the file (in lower case) that the pawn is on, followed by a lower-case "x" and then the file where the pawn moves. For example, `exd5` (pawn on the e-file captures the piece on d5).

- En passant captures are indicated by specifying the capturing pawn's file of departure, the "x", the destination square (not the square of the captured pawn), and (optionally) the suffix "e.p." indicating the capture was en passant. For example, `exd6 e.p`.

- Castling kingside is recorded as "0-0," while castling queenside is "0-0-0." The number of zeros indicates how many squares the rook has moved.

- When a king is attacked or threatened, it is known as check, which is notated as "+" at the end of the move.

- Checkmate is notated with a "#" at the end of the move. Fool's mate occurs after the moves `1. f3 e5 2. g4 Qh4#`. 

- After a game is over, the result also has special notation. If White wins, then it is notated as `1-0`. If Black wins, it is notated as `0-1`, while a draw is notated as `1/2-1/2`. 

- In some positions, two of the same piece (such as two knights) can be moved to the same square. In this case, you  write the piece abbreviation and append the **file** that the piece is on before you write the square. If the knight on f3 moves to d2, this move would be notated as `Nfd2`.

- If two pieces of the same type can both move to the same square AND they are already on the same file. In this case, you still start with the piece abbreviation and then append the **rank** of the piece before noting the square where it moves. If the knight on f3 moves to d2, the annotation is `N3d2`, while if the knight on f1 moves to d2, the annotation is `N1d2`.

## Portable Game Notation (PGN)<sup>[^fn3]</sup>

PGN (short for Portable Game Notation) is the standard format for recording a game in a text file that is processible by computers. Moves are recorded in algebraic notation, and comments can be inserted after a ";" symbol or between parentheses or curly brackets.

Example:
```
[Event "Third Rosenwald Trophy"]
[Site "New York, NY USA"]
[Date "1956.10.17"]
[EventDate "1956.10.07"]
[Round "8"]
[Result "0-1"]
[White "Donald Byrne"]
[Black "Robert James Fischer"]
[ECO "D92"]
[WhiteElo "?"]
[BlackElo "?"]
[PlyCount "82"]

1. Nf3 Nf6 2. c4 g6 3. Nc3 Bg7 4. d4 O-O 5. Bf4 d5 6. Qb3 dxc4 7. Qxc4 c6 8. e4 Nbd7 9. Rd1 Nb6 10. Qc5 Bg4 11. Bg5 Na4 12. Qa3 Nxc3 13. bxc3 Nxe4 14. Bxe7 Qb6 15. Bc4 Nxc3 16. Bc5 Rfe8+ 17. Kf1 Be6 18. Bxb6 Bxc4+ 19. Kg1 Ne2+ 20. Kf1 Nxd4+ 21. Kg1 Ne2+ 22. Kf1 Nc3+ 23. Kg1 axb6 24. Qb4 Ra4 25. Qxb6 Nxd1 26. h3 Rxa2 27. Kh2 Nxf2 28. Re1 Rxe1 29. Qd8+ Bf8 30. Nxe1 Bd5 31. Nf3 Ne4 32. Qb8 b5 33. h4 h5 34. Ne5 Kg7 35. Kg1 Bc5+ 36. Kf1 Ng3+ 37. Ke1 Bb4+ 38. Kd1 Bb3+ 39. Kc1 Ne2+ 40. Kb1 Nc3+ 41. Kc1 Rc2# 0-1
```

## Forsyth-Edwards Notation (FEN)<sup>[^fn4]</sup>

FEN is the abbreviation of Forsyth-Edwards Notation, and it is the standard notation to describe the state of a chess game. FEN sequences are composed exclusively of ASCII characters. These strings have six different fields, each separated by a space character.

1. Piece placement data: Each rank is described, starting with rank 8 and ending with rank 1, with a "/" between each one; within each rank, the contents of the squares are described in order from the a-file to the h-file. Each piece is identified by a single letter in algebraic notation (pawn = "P", knight = "N", bishop = "B", rook = "R", queen = "Q" and king = "K"). White pieces are designated using uppercase letters ("PNBRQK"), while black pieces use lowercase letters ("pnbrqk"). A set of one or more consecutive empty squares within a rank is denoted by a digit from "1" to "8", corresponding to the number of squares.

2. Active Color: Indicates who moves next. "w" specifies that it is White's turn to move, while "b" indicates that Black plays next.

3. Castling Rights: If neither side has the ability to castle, this field uses the character "-". Otherwise, this field contains one or more letters: "K" if White can castle kingside, "Q" if White can castle queenside, "k" if Black can castle kingside, and "q" if Black can castle queenside. 

4. Possible En Passant Targets: This is a square over which a pawn has just passed while moving two squares; it is given in algebraic notation. If there is no en passant target square, this field uses the character "-".

5. Halfmove Clock: The number of halfmoves since the last capture or pawn advance, used for the fifty-move rule.

6. Fullmove Number: The number of the full moves. It starts at 1 and is incremented after Black's move.

Example: After the move 1.e4
```
rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1
```
## Universal Chess Interface
The Universal Chess Interface (UCI) is an open communication protocol that enables chess engines to communicate with user interfaces. 

Examples:
```
e2e4
e7e5
e1g1 (white short castling)
e7e8q (for promotion)
```

[^fn1]: https://www.chess.com/terms/chess-notation
[^fn2]: https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
[^fn3]: https://www.chess.com/terms/chess-pgn
[^fn4]: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation