#include <iostream>
#include <string>

#include "chess.hpp"
#include "utils.hpp"
#include "negamax.hpp"

using namespace std;
using namespace chess;

int main() {
    string name;
    int age;
    char repeat;

    // Interactive loop
    do {
        // Greeting and input
        cout << "Welcome to the Interactive C++ Program!" << endl;
        cout << "Please enter your name: ";
        cin >> name;

        cout << "Hi " << name << "! How old are you? ";
        cin >> age;

        // Process input and provide output
        if (age < 18) {
            cout << "You're still young, " << name << "! Enjoy your youth!" << endl;
        } else if (age >= 18 && age < 60) {
            cout << "You're at a great stage in life, " << name << "!" << endl;
        } else {
            cout << "You're full of wisdom, " << name << "! Share your experiences." << endl;
        }

        // Ask to repeat
        cout << "Do you want to try again? (y/n): ";
        cin >> repeat;

    } while (repeat == 'y' || repeat == 'Y');

    cout << "Thank you for using the program. Goodbye!" << endl;
    return 0;
}