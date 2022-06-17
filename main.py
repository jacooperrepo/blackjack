"""initiate a new game"""
from library.game.blackjack import Blackjack, Spanish21, FaceUp21

if __name__ == '__main__':
    game = FaceUp21(2)
    game.play()

