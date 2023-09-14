from dataclasses import dataclass
from typing import Tuple
from .key import Key
from .Cards import Card

@dataclass
class Player:
    user_name: str
    password: str
    hand: Tuple[Card]