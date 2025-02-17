#include "givescore.h"
#include <iostream>


using namespace std;


int Game::Player::set_score()  {
	if(find_royal_flush())
		  score = 9;
	else if(find_straight_flush())
		  score = 8;
	else if(find_poker())
		  score = 7;
	else if(find_full_house())
		  score = 6;
	else if(find_flush())
		  score = 5;
	else if(find_straight())
		  score = 4;
	else if(find_three())
		  score = 3;
	else if(find_two_pair())
		  score = 2;
	else if(find_two())
		  score = 1;
	else	{
		score = 0;
		find_high_card();
	}
	
	return score; 
}

bool Game::Player::find_royal_flush()   {
    sort(cards.begin(), cards.end());
    int find {8};
    int cur_col {(*cards.begin())/13};
    for(const auto& x : cards) {
        if(x%13 == find  && cur_col == x/13 && find < 12)   {
            find++;
            topfive.push_back(x);
        } else if(x%13 == find && cur_col == x/13)    {
        		topfive.push_back(x);
            return true;
        } else {
        		topfive.clear();
            if(x%13 == 8)	{
                find = 9;
                topfive.push_back(x);
            }	else    {
                find = 8;
            }
            cur_col = x/13;
        }
    }
    topfive.clear();
    return false;
}

bool Game::Player::find_straight_flush()	{
	sort(cards.begin(), cards.end(), greater<int>());
    int find {(*cards.begin())%13};
    int cur_col {(*cards.begin())/13};
    int counter {0};
    for(const auto& x : cards) {
        if(x%13 == find  && cur_col == x/13)   {
            find--;
            topfive.push_back(x);
            counter++;
        	if(counter == 5)    {
            return true;
            }
        } else {
        		topfive.clear();
        		topfive.push_back(x);
            find = (x-1)%13;
            cur_col = x/13;
            counter = 1;
        }
    }
    topfive.clear();
    return false;
}


bool Game::Player::find_poker()	{
	sort(cards.begin(), cards.end(), [] (int a, int b) { return a%13 > b%13;});
	int counter {0};
	int value {*(cards.begin())%13};
	for(size_t i {0}; i < cards.size(); i++)	{
		if(value == cards.at(i)%13)	{
			counter++;
			topfive.push_back(cards.at(i));
			 if(counter >= 4)	{
			 	for(const auto& x : cards)	{
			 		bool isnew {true};
			 		for(const auto& y : topfive)	{
			 			if(x == y)	{
			 				isnew = false;
			 				break;
			 			}
			 		}
			 		if(isnew)	{
			 			topfive.push_back(x);
			 			break;
			 		}
			 	}
			 	return true;
			 	}
		} else {
		topfive.clear();
			counter = 1;
			value = cards.at(i);
			topfive.push_back(cards.at(i));
		}
	}
	topfive.clear();
	return false;
}

bool Game::Player::find_full_house()	{
 vector<int> tmp {cards};
	sort(cards.begin(), cards.end(), [] (int a, int b) { return a%13 > b%13;});
	int counter {0};
	int value {*(cards.begin())%13};
	for(const auto& x : cards)	{
		if(value == x%13)	{
			counter++;
			topfive.push_back(x);
			if(counter == 3)	{
				for(size_t i {1}; i < cards.size(); i++)	{
					if(cards.at(i-1)%13 != x%13 && cards.at(i-1)%13 == cards.at(i)%13)	{
						topfive.push_back(cards.at(i-1));
						topfive.push_back(cards.at(i));
						return true;
					}
				}
			}
		 
		} else {
		topfive.clear();
		topfive.push_back(x);
			counter = 1;
			value = x%13;
		}
	}
	topfive.clear();
	return false;
}



bool Game::Player::find_flush()	{
	sort(cards.begin(), cards.end(), [] (int a, int b) {return a > b;});
	int color_counter {0};
	int cur_color {0};
	for(const auto& x : cards)	{
		if(x/13 == cur_color && color_counter < 4)	{
			color_counter++;
			topfive.push_back(x);
		} else if(x/13 == cur_color)	{
			topfive.push_back(x);
			return true;
		} else {
		color_counter = 1;
		cur_color = x/13;
		topfive.clear();
		topfive.push_back(x);
		}
	}
	topfive.clear();
	return false;
}

bool Game::Player::find_straight()	{//Returns the latter of two cards, why? Don't know!
	
	sort(cards.begin(), cards.end(), [] (int a, int b) { return a%13 > b%13;});
	int str_counter {0};
	int find {(*cards.begin())%13};

	for(const auto& card : cards)	{
		if(card%13 == find && str_counter < 4)	{
			find--;
			str_counter++;
			topfive.push_back(card);
			
		} else if(card%13 == find+1)	{
			;
		} else if(card%13 == find)	{
			topfive.push_back(card);
			return true;
		}	else {
			topfive.clear();
			topfive.push_back(card);
			str_counter = 1;
			find = (card%13)-1;
		}
	}
	return false;
}

bool Game::Player::find_three()	{
	sort(cards.begin(), cards.end(), [] (int a, int b) { return a%13 > b%13;});
	int counter {0};
	int value {*(cards.begin())%13};
	for(const auto& x : cards)	{
		if(value == x%13)	{
			counter++;
			topfive.push_back(x);
			 if(counter >= 3)	{
			 	for(const auto& y : cards)	{
			 		if(y%13 != value)
			 			topfive.push_back(y);
			 		if(topfive.size() >= 5)
			 			break;
			 	}
			 	return true;
			 }
		} else {
		topfive.clear();
		topfive.push_back(x);
			counter = 1;
			value = x%13;
		}
	}
	topfive.clear();
	return false;
}

bool Game::Player::find_two_pair()  {
    sort(cards.begin(), cards.end(), [] (int a, int b) { return a%13 > b%13;});
    int pair_count {0};
    for(size_t i {1}; i < cards.size(); i++)   {
        if(cards.at(i-1)%13 == cards.at(i)%13 && pair_count < 1)    {
            pair_count++;
            topfive.push_back(cards.at(i-1));
            topfive.push_back(cards.at(i));
        } else if(cards.at(i-1)%13 == cards.at(i)%13)   {
        		topfive.push_back(cards.at(i-1));
            topfive.push_back(cards.at(i));
            for(const auto& x : cards)	{
            	if(x%13 != topfive.at(0)%13 && x%13 != topfive.at(2)%13)	{
            		topfive.push_back(x);
            		break;	
            	}
            }
            return true;
        }
    }
    topfive.clear();
    return false;
}

bool Game::Player::find_two()	{
	sort(cards.begin(), cards.end(), [] (int a, int b) { return a%13 > b%13;});
	int counter {0};
	int value {*(cards.begin())};
	for(const auto& x : cards)	{
		if(value == x%13)	{
			counter++;
			topfive.push_back(x);
			 if(counter >= 2)	{
			 	for(const auto& y : cards)	{
			 		if(y%13 != x%13)	{
			 			topfive.push_back(y);
			 		}
			 		if(topfive.size() >= 5)
			 			break;
			 	}
			 	return true;
			 }
		} else {
			topfive.clear();
			topfive.push_back(x);
			counter = 1;
			value = x%13;
		}
	}
	topfive.clear();
	return false;
}

void Game::Player::find_high_card()	{
	sort(cards.begin(), cards.end(), [] (int a, int b) { return a%13 > b%13;});
	topfive.clear();
	for(size_t i {0}; i < 5; i++)	{
		topfive.push_back(cards.at(i));
	}
}

int Game::Player::compare_topfive(vector<int> topfive) {
	for (int i = 0; i < this->topfive.size(); i++) {
		if (topfive[i]%13 < this->topfive[i]%13) {
			return 1;
		}
		if (topfive[i]%13 > this->topfive[i]%13) {
			return -1;
		}
	}
	return 0;
}

vector<int> Game::score_players() {
	vector<int> scores;
	for (Player& player : this->players) {
		scores.push_back(player.set_score());
	}
	return scores;
}

vector<int> Game::determine_winners()	{
	vector<int> scores = this->score_players();
	vector<int> winners;
	vector<int> highcard_winners;
	int max_score = 0;
	for (int i = 0; i < scores.size();i++)	{
		if(scores[i] > max_score) {
			winners.clear();
			winners.push_back(i);
			max_score = scores[i];
		}else if(scores[i] == max_score) {
			winners.push_back(i);
		}
	}
	//eliminate winners with lower highcards
	for (int i = 0; i < winners.size(); i++) {
		if (highcard_winners.size() == 0) {
			highcard_winners.push_back(winners[i]);
		} else {
			int comparison = this->players[winners[i]].compare_topfive(this->players[highcard_winners[highcard_winners.size() - 1]].get_topfive());
			if(comparison == 1) {
				highcard_winners.clear();
			}
			if (comparison >= 0) {
				highcard_winners.push_back(winners[i]);
			}
		}
		
	}
	return highcard_winners;
}























