#pragma once
#include "chess.hpp"

int larry_kaufman_piece_sum(chess::Board&, chess::Color);

chess::Move negamax(chess::Board& board, int (*eval_func)(chess::Board&, chess::Color), chess::Color player_color, int depth);

class MiniMaxAgent {
    public:
        enum class TTFlag { EXACT = 1, UPPERBOUND = 2, LOWERBOUND = 3 };

        struct TTEntry {
            TTFlag flag;
            float value;
            int depth;
            chess::Move move;
        };

        // Constructor
        MiniMaxAgent() = default;

        // Destructor
        ~MiniMaxAgent() = default;

        // Reset the transposition table
        void reset_transposition_table();

        // Negamax function
        chess::Move negamax(chess::Board& board, int (*eval_func)(chess::Board&, chess::Color), chess::Color player_color, int depth);

    private:
        // Private member variables
        std::unordered_map<uint64_t, TTEntry> transposition_table;
};