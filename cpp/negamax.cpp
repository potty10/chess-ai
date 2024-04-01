#include <limits>
#include "chess.hpp"
#include "utils.hpp"
#include "negamax.hpp"

using namespace chess;

const int WIN_VALUE = 9999999;
const int DRAW_VALUE = 0;
const float POSTIIVE_INFINITY = std::numeric_limits<float>::infinity();
const float NEGATIVE_INFINITY = -std::numeric_limits<float>::infinity();

int larry_kaufman_piece_sum(Board &board, Color maximising_player) {
    
    std::unordered_map<PieceType, int, EnumClassHash> piece_value = {
        {PieceType::PAWN, 100},
        {PieceType::BISHOP, 325},
        {PieceType::KNIGHT, 325},
        {PieceType::ROOK, 500},
        {PieceType::QUEEN, 975},
        {PieceType::KING, 0}, // King has no value
        {PieceType::NONE, 0},
    };

    int result = 0;
    std::array<int, 2> bishop_count = {0, 0}; // (white bishop, black bishop)

    for (int i = 0; i < 64; ++i) {
        Piece piece = board.at(Square(i));
        if (piece.type() != PieceType::NONE) {
            if (piece.color() == Color::WHITE) {
                result += piece_value[piece.type()];
            } else {
                result -= piece_value[piece.type()];
            }
        }
    }
    
    if (maximising_player == Color::WHITE) {
        return result;
    }
    return -result;
}

Move negamax(Board& board, int (*eval_func)(Board&, Color), Color player_color, int depth=2) 
{
    auto _negamax = [&board, &eval_func](int depth, int color, float alpha, float beta, const auto& _negamax) -> std::pair<Move, float>
    {
        auto outcome = board.isGameOver().second;
        if (outcome == GameResult::DRAW) return std::pair(NULL, DRAW_VALUE);
        bool is_white_win = (outcome == GameResult::WIN && board.sideToMove() == Color::WHITE) || 
            (outcome == GameResult::LOSE && board.sideToMove() == Color::BLACK);       
        if (is_white_win) return std::pair(NULL, color * WIN_VALUE);
        bool is_black_win = (outcome == GameResult::WIN && board.sideToMove() == Color::BLACK) || 
            (outcome == GameResult::LOSE && board.sideToMove() == Color::WHITE);
        if (is_black_win) return std::pair(NULL, - color * WIN_VALUE);

        if (depth == 0) return std::pair(NULL, color * eval_func(board, Color::WHITE));

        float best_move_value = NEGATIVE_INFINITY;
        Move best_move;

        Movelist moves;
        movegen::legalmoves(moves, board);
        for (const auto &move : moves) {
            board.makeMove(move);
            auto [current_move, current_value] = _negamax(depth - 1, -color, -beta, -alpha, _negamax); // Use recursive lambdas
            current_value = - current_value;
            board.unmakeMove(move);

            if (current_value > best_move_value) {
                best_move = move;
                best_move_value = current_value;
            }

            if (best_move_value > beta) {
                return std::pair(best_move, best_move_value);
            }

            alpha = std::max(alpha, best_move_value);
        }

        return std::pair(best_move, best_move_value);
    };

    int color = player_color == Color::WHITE? 1 : -1;
    auto [current_move, current_value] = _negamax(depth, color, NEGATIVE_INFINITY, POSTIIVE_INFINITY, _negamax);
    return current_move;
}


Move MiniMaxAgent::negamax(Board& board, int (*eval_func)(Board&, Color), Color player_color, int depth=2) 
{
    // Capturing private class member in lamabda using "this"
    auto _negamax = [&board, &eval_func, this](int depth, int color, float alpha, float beta, const auto& _negamax) -> std::pair<Move, float>
    {
        float alpha_original = alpha;

        auto tt_key = board.hash();
        if (transposition_table.find(tt_key) != transposition_table.end() && transposition_table[tt_key].depth >= depth) {
            auto& tt_entry = transposition_table[tt_key];
            if (tt_entry.flag == TTFlag::EXACT)
                return { tt_entry.move, tt_entry.value };
            else if (tt_entry.flag == TTFlag::LOWERBOUND)
                alpha = std::max(alpha, tt_entry.value);
            else if (tt_entry.flag == TTFlag::UPPERBOUND)
                beta = std::min(beta, tt_entry.value);
            if (alpha >= beta)
                return { tt_entry.move, tt_entry.value };
        }

        auto outcome = board.isGameOver().second;
        if (outcome == GameResult::DRAW) return std::pair(NULL, DRAW_VALUE);
        bool is_white_win = (outcome == GameResult::WIN && board.sideToMove() == Color::WHITE) || 
            (outcome == GameResult::LOSE && board.sideToMove() == Color::BLACK);       
        if (is_white_win) return std::pair(NULL, color * WIN_VALUE);
        bool is_black_win = (outcome == GameResult::WIN && board.sideToMove() == Color::BLACK) || 
            (outcome == GameResult::LOSE && board.sideToMove() == Color::WHITE);
        if (is_black_win) return std::pair(NULL, - color * WIN_VALUE);

        if (depth == 0) return std::pair(NULL, color * eval_func(board, Color::WHITE));

        float best_move_value = NEGATIVE_INFINITY;
        Move best_move;

        Movelist moves;
        movegen::legalmoves(moves, board);
        for (const auto &move : moves) {
            board.makeMove(move);
            auto [current_move, current_value] = _negamax(depth - 1, -color, -beta, -alpha, _negamax); // Use recursive lambdas
            current_value = - current_value;
            board.unmakeMove(move);

            if (current_value > best_move_value) {
                best_move = move;
                best_move_value = current_value;
            }

            if (best_move_value > beta) {
                return std::pair(best_move, best_move_value);
            }

            alpha = std::max(alpha, best_move_value);
        }

        TTFlag newflag = TTFlag::EXACT;
        if (best_move_value <= alpha_original)
            newflag = TTFlag::UPPERBOUND;
        else if (best_move_value >= beta)
            newflag = TTFlag::LOWERBOUND;
        TTEntry new_tt_entry{newflag, best_move_value, depth, best_move};
        transposition_table[tt_key] = new_tt_entry;


        return std::pair(best_move, best_move_value);
    };

    int color = player_color == Color::WHITE? 1 : -1;
    auto [current_move, current_value] = _negamax(depth, color, NEGATIVE_INFINITY, POSTIIVE_INFINITY, _negamax);
    return current_move;
};