"""initiate a new game"""
from src.game.blackjack import BlackjackGameCollection

if __name__ == '__main__':
    games = BlackjackGameCollection()
    games.select_game()

