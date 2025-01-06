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
        if (user_input.rfind("depth ", 0) != 0) {
            cout << "Expected depth command" << endl;   
        }
        int depth = atoi(user_input.substr(6).c_str());
        getline(cin, user_input);
        if (user_input.rfind("fen ", 0) != 0) {
            cout << "Expected fen command" << endl;   
        }
        string fen = user_input.substr(4);
        Board board(fen); // User input is chess fen
        Color color = board.sideToMove();
        Move move = negamax_agent.negamax(board, larry_kaufman_piece_sum, color, 3);
        cout << uci::moveToUci(move) << endl;
    }

    return 0;
}