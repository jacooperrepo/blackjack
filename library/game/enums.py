"""Enumerations for the blackjack game"""
from enum import Enum


class GameWinner(Enum):
    """Indication of winner in game"""
    NotSet: str = "NotSet"
    Player: str = "Player"
    Dealer: str = "Dealer"
    Draw: str = "Draw"


class PlayerHandStatus(Enum):
    """Status of player hand in blackjack game"""
    InPlay: str = "InPlay"
    SplitInPlayHandOne: str = "SplitInPlayHandOne"
    SplitInPlayHandTwo: str = "SplitInPlayHandTwo"
    SplitEnded: str = "SplitEnded"
    Ended: str = "Ended"


