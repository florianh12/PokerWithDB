from enum import Enum, unique

@unique
class State(Enum):
    raise_ = 'RAISE'
    bet = 'BET'
    fold = 'FOLD'
    unkown = 'UNKNOWN'