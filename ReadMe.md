# Table of Contents
1. [Introduction](#example)
2. [Chess Programming](#chess-programming)
    - [Heuristics](#heuristics)
    - [Move Ordering](#move-ordering)
    - [Transposition Tables](#transposition-tables)
3. [Evaluation](#evaluation)
4. [Development](#references)

## Introduction
This is an implementation of a chess computer with Alpha Beta pruning.
## Chess Programming
#### Guaranteeing checkmate
Minimax algorithm needs to evaluate terminal nodes as infinity or a large number.
#### Heuristics
Heuristics are needed because it is impossible to evaluate at depth.
#### Move Ordering
Move ordering is the first enhancement of Alpha-Beta Pruning. Instead of randomly choose a position or move from the list of possible ones and evaluate it, the computer sorts them beforehand. The good news: Evaluating good moves and positions first, the Alpha-Beta Pruning can cut more branches and therefore can evaluate more positions in advance.
#### Transposition Tables
The third enhancement we implemented are transposition tables. In chess there are many transpositions. Assume that player A can make a a1 on which the player B reacts with b1. Player A now can make an independent move a2 where player B reacts with b2. The two resulting sequences `[a1, b1, a2, b2]` and `[a2, b2, a1, b1]` are transpositions leading to the same position. If the first sequence was already evaluated, it is good to store the result in a hash table. When the second sequence needs to be evaluated, the already computed result can be used instead of re-calculating it. This safes a lot of time!
#### Forcing a draw
The opponent can use the fivefold repitition rule or the 75 move rule to force a draw.
#### Zobrist hashing

## Evaluation
We first have a set of chess bots and play them against each other. We calculate the ELO from the results of these matches using the Beyesian Elo
Rating algorithm: https://www.remi-coulom.fr/Bayesian-Elo. 

Links to ELO system:
- https://www.cantorsparadise.com/the-mathematics-of-elo-ratings-b6bfc9ca1dba
- https://www.reddit.com/r/chess/comments/q4x477/retroactive_elo_calculator_using_a_data_set_of/
- https://github.com/michiguel/Ordo?tab=readme-ov-file

Links to engines:
- https://www.chess.com/forum/view/general/chess-program-with-variable-difficulty
## Development
Use this link: [https://www.chess.com/analysis?tab=analysis](https://www.chess.com/analysis?tab=analysis) to visualise the game. Just input the FEN to get the current state of the board, or input the entire match in algebraic notation to get the whole match.

Use this link: [https://github.com/lichess-bot-devs/lichess-bot?tab=readme-ov-file](https://github.com/lichess-bot-devs/lichess-bot?tab=readme-ov-file) to play the bot against real human players on lichess.
Takes a long time to find a match.
## References
https://florian-dahlitz.de/articles/building-a-chess-computer-using-python
https://stackoverflow.com/questions/59647151/minimax-with-alhpa-beta-pruning-for-chess
https://github.com/AnthonyASanchez/python-chess-ai/blob/master/AlphaBetaPruning.py