#ifndef GIVESCORE_H
#define GIVESCORE_H


#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <iostream>
#include <stdexcept>


using namespace std;


class Game {
	class Player;
	vector<Player> players;
	vector<Player> winners;
	vector<int> table;

public:
	Game(vector<int> table, vector<int> player_handcards)	: winners{}, table{table} {
		if (player_handcards.size()%2 != 0) {
			throw std::runtime_error("Player handcards have to be even");
		}

		for(int i = 0; i < player_handcards.size(); i += 2) {
			vector<int> cards {this->table}; 
			cards.push_back(player_handcards.at(i));
			cards.push_back(player_handcards.at(i+1));
			this->players.push_back(Player(cards));
		}
	}
	
	vector<Player> get_players() {return players;}
	vector<int> get_table() {return table;}

	vector<int> score_players(); //WIP
	vector<int> get_scores();
	vector<int> determine_winners(); //WIP

	private:
	class Player {
		int score {0};
		vector<int> cards;
		vector<int> hand;
		vector<int> topfive;
		
		bool find_royal_flush();
		bool find_straight_flush();
		bool find_poker();
		bool find_full_house();
		bool find_flush();
		bool find_straight();
		bool find_three();
		bool find_two_pair();
		bool find_two();
		void find_high_card();
	public:
		Player(vector<int> cards)	: score{0}, cards{cards}, hand{cards.end() - 2, cards.end()}, topfive{}	{}
		
		int get_score()	{return score;}//Debug function/system function
		vector<int> get_cards() const	{return cards;} //Debug function/system function
		vector<int> get_topfive() {return topfive;}//Debug function/system function
		vector<int> get_hand() const	{return hand;}

		int compare_topfive(vector<int> topfive); // returns -1 for smaller 0 for equal and 1 for bigger
		int set_score();
	};
};




#endif //GIVESCORE_H
