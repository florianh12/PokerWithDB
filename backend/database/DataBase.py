from abc import ABC, abstractmethod
from typing import List, Tuple
from models import *

class DataBase(ABC):

    @abstractmethod
    def create_player(self, player: Player) -> None:
        pass

    @abstractmethod
    def create_game(self, players: Player) -> None:
        pass

    @abstractmethod
    def get_games(self, player:Player) -> List[Game]:
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