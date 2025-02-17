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





























	/*
	bool find1 {false};
	bool find2 {false};
	
	int MIN {0};
	int MAX {51};

	long long int round {0};

	random_device rd;
	default_random_engine reng(rd());
	uniform_int_distribution<int> distr(MIN, MAX);

	vector<int> player2;
	vector<int> player1;


	while(!find1 && !find2)	{
	
		vector<int> deck {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51};
		
		MIN = 0;
		MAX = 51;
		
		player1.clear();
		player2.clear();
		distr.param(uniform_int_distribution<int>::param_type(MIN,MAX));
		round += 2;


		for(size_t i {0}; i < 5; i++)	{
			int tmp {distr(reng)};
			player1.push_back(deck.at(tmp));
			player2.push_back(deck.at(tmp));
			deck.erase(deck.begin() + tmp);
			MAX--;
			distr.param(uniform_int_distribution<int>::param_type(MIN,MAX));
		}

		for(size_t i {0}; i < 2; i++)	{
			int tmp {distr(reng)};
			player1.push_back(deck.at(tmp));
			deck.erase(deck.begin() + tmp);
			MAX--;
			distr.param(uniform_int_distribution<int>::param_type(MIN,MAX));
		}

		for(size_t i {0}; i < 2; i++)	{
			int tmp {distr(reng)};
			player2.push_back(deck.at(tmp));
			deck.erase(deck.begin() + tmp);
			MAX--;
			distr.param(uniform_int_distribution<int>::param_type(MIN,MAX));
		}
		
		find_high_card(player1);
		find1 = true;
		find2 = get_score(player2) == 3;
	}


	sort(player1.begin(), player1.end());
	sort(player2.begin(), player2.end());


	for(const auto& x : player1)	{
		cout << convert(x);
	}
	
	cout << "High Cards: ";
	for(const auto& x : find_high_card(player1))	{
		cout << convert(x);
	}

	cout << get_score(player1) << '\n';

	for(const auto& x : player2)	{
		cout << convert(x);
	}

	cout << get_score(player2) << '\n';

	cout << round << " trys\n";
	*/
	
	return 0;
	}
	
	
