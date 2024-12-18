#include <iostream>
#include <string>

#include "chess.hpp"
#include "utils.hpp"
#include "negamax.hpp"

using namespace std;
using namespace chess;

int main() {
    MiniMaxAgent negamax_agent;    
    string user_input;

    // Interactive loop
    while (true) {
        getline(cin, user_input);
        if (user_input == "quit") break;
        Board board(user_input); // User input is chess fen
        Color color = board.sideToMove();
        Move move = negamax_agent.negamax(board, larry_kaufman_piece_sum, color, 3);
        cout << uci::moveToUci(move) << endl;
    }

    return 0;
}