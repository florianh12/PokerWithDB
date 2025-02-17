#include "givescore.h"

#include <iostream>
#include <vector>

#include <map>
#include <string>
#include <algorithm>
#include <stdexcept>

using namespace std;





int main(int argc, char* argv[]) {
//if incorrect amount of cards is given (5 table cards and 2 Player handcards) program terminates with -1
if(argc < 8 || argc%2 != 0)
	return -1;

vector<int> table {stoi(argv[1]),stoi(argv[2]),stoi(argv[3]),stoi(argv[4]),stoi(argv[5])};
vector<int> player_handcards;

for (size_t i = 6; i < argc; i++) {
	player_handcards.push_back(stoi(argv[i]));
}

//assurance that everything did go according to plan
if (player_handcards.size()%2 != 0) {
	throw runtime_error("Not all players have 2 handcards");
}


Game test = Game(table, player_handcards);
vector<int> scores = test.determine_winners();
for (auto& score : scores) {
	cout << score << "\n";
}
	
	return 0;
	}
	
	
