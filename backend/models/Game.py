from dataclasses import dataclass
from typing import List
from .key import Key
from .Player import Player
from .Cards import Card

@dataclass
class Game:
    _id: Key
    table: List[Card]