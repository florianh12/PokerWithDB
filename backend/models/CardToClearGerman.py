from .Cards import Card
from .CardToClear import CardToClear

class CardToClearGerman(CardToClear):
    color = {0: "Herz", 1: "Pik", 2: "Karo", 3: "Treff"}
    symbol = {0: "Zwei", 1: "Drei", 2: "Vier", 3: "Fünf", 4: "Sechs", 5: "Sieben", 6: "Acht", 7: "Neun", 8: "Zehn", 9: "Bube", 10: "Dame", 11: "König", 12: "Ass"}
    
    @staticmethod
    def translate(card: Card) -> str:
        return CardToClearGerman.color.get(int(card.value/13), "Color not found!") + " " + CardToClearGerman.symbol.get(card.value%13, "Symbol not found!")
    
