"""Enumerations for the blackjack game"""
from enum import Enum


class GameWinner(Enum):
    """Indication of winner in game"""
    NOTSET: str = "NotSet"
    PLAYER: str = "Player"
    DEALER: str = "Dealer"
    DRAW: str = "Draw"


class PlayerHandStatus(Enum):
    """Status of player hand in blackjack game"""
    IN_PLAY: str = "InPlay"
    SPLIT_IN_PLAY_HAND_ONE: str = "SplitInPlayHandOne"
    SPLIT_IN_PLAY_HAND_TWO: str = "SplitInPlayHandTwo"
    SPLIT_ENDED: str = "SplitEnded"
    ENDED: str = "Ended"
