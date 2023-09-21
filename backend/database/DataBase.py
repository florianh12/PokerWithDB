from abc import ABC, abstractmethod
from typing import List
from models import Player, Game

class DataBase(ABC):

    @abstractmethod
    def create_player(self, username:str, password:str) -> None:
        pass

    @abstractmethod
    def create_game(self, players: List[str]) -> None:
        pass

    @abstractmethod
    def get_games(self, username:str) -> List[Game]:
        pass

    @abstractmethod
    def get_players(self, game:Game) -> List[Player]:
        pass
    
    @abstractmethod
    def login(self, username:str, pwd:str) -> bool:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass