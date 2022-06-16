"""initiate a new game"""
from library.game.blackjack import Blackjack

if __name__ == '__main__':
    game = Blackjack(2)
    game.play()
