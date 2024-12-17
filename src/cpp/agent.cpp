#include <iostream>
#include <string>

#include "chess.hpp"
#include "utils.hpp"
#include "negamax.hpp"

using namespace std;
using namespace chess;

int main() {
    MiniMaxAgent negamax_agent;    
    string fen;

    // Interactive loop
    while (true) {
        cin >> fen;
        Board board(fen);
        Color color = board.sideToMove();
        Move move = negamax_agent.negamax(board, larry_kaufman_piece_sum, color, 3);
        cout << uci::moveToSan(board, move) << endl;
    }

    return 0;
}