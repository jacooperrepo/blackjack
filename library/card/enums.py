"""Enumerations for cards"""
from enum import Enum


class CardSuit(Enum):
    """Card suits"""
    Hearts: str = "Hearts"
    Clubs: str = "Clubs"
    Spades: str = "Spades"
    Diamonds: str = "Diamonds"
    Joker: str = "Joker"


class CardValue(Enum):
    """Card values"""
    Joker: str = '🃏'
    Ace: str = 'A'
    Two: str = '2'
    Three: str = '3'
    Four: str = '4'
    Five: str = '5'
    Six: str = '6'
    Seven: str = '7'
    Eight: str = '8'
    Nine: str = '9'
    Ten: str = '10'
    Jack: str = 'J'
    Queen: str = 'Q'
    King: str = 'K'