#include <time.h> 
#include <vector>
#include <fstream>
#include <chrono>
#include <math.h>
#include <iomanip>
#include <ctime>

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

std::string get_current_timestamp() {
    auto now = std::chrono::system_clock::now();
    std::time_t now_c = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&now_c), "%Y-%m-%d-%H-%M-%S");   
    return ss.str();
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

    float time_multiple = (1 << 10) / pow(10, 3); //

    std::vector<int> win_count = {0, 0}; // white, black
    for (int test_case = 0; test_case < no_games; ++test_case) {
        Board board;
        int n = 1;
        std::stringstream move_history;

        MiniMaxAgent negamax_agent_white;
        MiniMaxAgent negamax_agent_black;

        while(true) {
            Move move;
            if (n % 2 == 1) {
                auto start = std::chrono::high_resolution_clock::now();
                move = negamax_agent_white.negamax(board, larry_kaufman_piece_sum, Color::WHITE, 4);
                auto stop = std::chrono::high_resolution_clock::now();
                result["White Time"] += std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count()  >> 10;
                // move = random_move(board);
            } else {
                auto start = std::chrono::high_resolution_clock::now();
                move = negamax_agent_black.negamax(board, larry_kaufman_piece_sum, Color::BLACK, 4);
                auto stop = std::chrono::high_resolution_clock::now();
                result["Black Time"] += std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count()  >> 10;
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

                result["Black Time"] *= time_multiple;
                result["White Time"] *= time_multiple;

                std::string filename = "output/" + get_current_timestamp() +".txt";

                std::ofstream outputFile(filename, std::ios_base::app);
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