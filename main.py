"""initiate a new game"""
from library.game.blackjack import BlackjackGameCollection

if __name__ == '__main__':
    games = BlackjackGameCollection(5, 150)
    games.select_game()

