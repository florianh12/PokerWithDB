from abc import ABC, abstractmethod
from .Cards import Card

class CardToClear(ABC):
    color = {0: "Not defined abstract class!", 1: "Not defined abstract class!", 2: "Not defined abstract class!", 3: "Not defined abstract class!"}
    symbol = {0: " ", 1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " ", 10: " ", 11: " ", 12: " "}
    
    @staticmethod
    def translate(card:Card) -> str:
        return CardToClear.color.get(int(card.value/13), "Color not found!") + " " + CardToClear.symbol.get(card.value%13, "Symbol not found!")