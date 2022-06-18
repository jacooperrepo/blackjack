"""Enumerations for blackjack"""
from enum import Enum


class CardSuit(Enum):
    """Card suits"""
    HEARTS: str = "Hearts"
    CLUBS: str = "Clubs"
    SPADES: str = "Spades"
    DIAMONDS: str = "Diamonds"
    JOKER: str = "Joker"


class CardValue(Enum):
    """Card values"""
    JOKER: str = '🃏'
    ACE: str = 'A'
    TWO: str = '2'
    THREE: str = '3'
    FOUR: str = '4'
    FIVE: str = '5'
    SIX: str = '6'
    SEVEN: str = '7'
    EIGHT: str = '8'
    NINE: str = '9'
    TEN: str = '10'
    JACK: str = 'J'
    QUEEN: str = 'Q'
    KING: str = 'K'
