"""Exceptions for the blackjack game"""


class OutOfFundsException(Exception):
    """Exception if player is out of funds"""
    def __init__(self):
        super().__init__()