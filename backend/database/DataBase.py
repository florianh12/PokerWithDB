from abc import ABC, abstractmethod
from typing import List
from models import Player, PokerGame, Plays

class DataBase(ABC):

    @abstractmethod
    def create_player(self, username:str, password:str) -> None:
        pass

    @abstractmethod
    def create_game(self, players: List[str], name: str = '') -> None:
        pass
    
    @abstractmethod
    def join_game(self, player:str, id = None, name = None) -> None:
        pass

    @abstractmethod
    def get_games(self, username:str) -> List[PokerGame]:
        pass

    @abstractmethod
    def get_players(self, game:PokerGame) -> List[Plays]:
        pass
    
    @abstractmethod
    def login(self, username:str, pwd:str) -> bool:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass