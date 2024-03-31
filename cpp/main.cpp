#include "chess.hpp"
#include <limits>
#include <time.h> 
#include <vector>
#include <fstream>
#include <chrono>
#include <math.h>

using namespace chess;

const int WIN_VALUE = 9999999;
const int DRAW_VALUE = 0;
const float POSTIIVE_INFINITY = std::numeric_limits<float>::infinity();
const float NEGATIVE_INFINITY = -std::numeric_limits<float>::infinity();

// https://stackoverflow.com/questions/18837857/cant-use-enum-class-as-unordered-map-key
struct EnumClassHash
{
    template <typename T>
    std::size_t operator()(T t) const
    {
        return static_cast<std::size_t>(t);
    }
};

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

std::pair<Move, float> _negamax(Board& board, int (*eval_func)(Board&, Color), int depth, int color, float alpha, float beta)
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
        auto [current_move, current_value] = _negamax(board, eval_func, depth - 1, -color, -beta, -alpha);
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

Move negamax(Board& board, int (*eval_func)(Board&, Color), Color player_color, int depth=2) 
{
    int color = player_color == Color::WHITE? 1 : -1;
    auto [current_move, current_value] = _negamax(board, larry_kaufman_piece_sum, depth, color, NEGATIVE_INFINITY, POSTIIVE_INFINITY);
    return current_move;
}

Move random_move(Board& board)
{
    Movelist moves;
    movegen::legalmoves(moves, board);
    Move move = moves[rand() % moves.size()];
    // std::cout << uci::moveToSan(board, move) << " ";
    return move;
}
int get_statistics(int no_games) 
{

    std::unordered_map<GameResultReason, std::string_view, EnumClassHash> termination_enums = {
        {GameResultReason::CHECKMATE, "CHECKMATE"},
        {GameResultReason::STALEMATE, "STALEMATE"},
        {GameResultReason::INSUFFICIENT_MATERIAL, "INSUFFICIENT_MATERIAL"},
        {GameResultReason::FIFTY_MOVE_RULE, "FIFTY_MOVE_RULE"},
        {GameResultReason::THREEFOLD_REPETITION, "THREEFOLD_REPETITION"},
    };

    std::vector<std::string_view> possible_results = { 
        "CHECKMATE", 
        "STALEMATE",
        "INSUFFICIENT_MATERIAL", 
        "FIFTY_MOVE_RULE", 
        "THREEFOLD_REPETITION",
        "Black Win",
        "White Win",
        "White Time",
        "Black Time"
    };

    std::unordered_map<std::string_view, int> result;

    for (auto& r: possible_results) {
        result[r] = 0;
    }


    std::vector<int> win_count = {0, 0}; // white, black
    for (int test_case = 0; test_case < no_games; ++test_case) {
        Board board;
        int n = 1;
        std::stringstream move_history;
        while(true) {
            Move move;
            if (n % 2 == 1) {
                auto start = std::chrono::high_resolution_clock::now();
                move = negamax(board, larry_kaufman_piece_sum, Color::WHITE, 2);
                auto stop = std::chrono::high_resolution_clock::now();
                result["White Time"] += duration_cast<std::chrono::microseconds>(stop - start).count() / pow(10, 6);
                // move = random_move(board);
            } else {
                auto start = std::chrono::high_resolution_clock::now();
                move = random_move(board);
                auto stop = std::chrono::high_resolution_clock::now();
                result["Black Time"] += duration_cast<std::chrono::microseconds>(stop - start).count() / pow(10, 6);
            }
            move_history << n << ". " << move << " ";
            board.makeMove(move);
                       
            n += 1;
            auto outcome = board.isGameOver().second;
            if (outcome != GameResult::NONE) {
                GameResultReason outcome_reason = board.isGameOver().first;
                result[termination_enums[outcome_reason]] += 1;
                bool is_white_win = (outcome == GameResult::WIN && board.sideToMove() == Color::WHITE) || 
                    (outcome == GameResult::LOSE && board.sideToMove() == Color::BLACK);       
                if (is_white_win) result["White Win"] += 1;
                bool is_black_win = (outcome == GameResult::WIN && board.sideToMove() == Color::BLACK) || 
                    (outcome == GameResult::LOSE && board.sideToMove() == Color::WHITE);
                if (is_black_win) result["Black Win"] += 1;

                
                std::ofstream outputFile("history.txt");
                if (!outputFile.is_open()) {
                    std::cerr << "Error: Unable to open the file." << std::endl;
                    return 1;
                }
                outputFile << "[Game " << test_case << "]\n";
                outputFile << "[" << termination_enums[outcome_reason] << "]\n";
                outputFile << move_history.str() << std::endl;
                outputFile.close();

                break;
            }
            
        }
    }
    std::cout << "RESULTS: \n";
    for (const auto& pair : result) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }
    return 0;
}
int main () {
    srand(time(0));
    get_statistics(1);
    return 0;
}