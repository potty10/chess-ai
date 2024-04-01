#include <time.h> 
#include <vector>
#include <fstream>
#include <chrono>
#include <math.h>
#include "chess.hpp"
#include "utils.hpp"
#include "negamax.hpp"

using namespace chess;

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

        MiniMaxAgent negamax_agent;

        while(true) {
            Move move;
            if (n % 2 == 1) {
                auto start = std::chrono::high_resolution_clock::now();
                move = negamax_agent.negamax(board, larry_kaufman_piece_sum, Color::WHITE, 5);
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

                
                std::ofstream outputFile("history.txt", std::ios_base::app);
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