# Testing deck
from Pack.deck import Deck, Diamonds, Joker, Spades
from Pack.card_attributes import CardSuit, CardValue

if __name__ == '__main__':

    deck = Deck(True)
    deck.shuffle()

    deck.deal()
    deck.deal()

    print(''.join(str(card) for card in deck.cards))

    deck.reset()

    print(''.join(str(card) for card in deck.cards))

    diamond = Diamonds(CardValue.King)
    deck.add(diamond)

    deck.remove(Spades(CardValue.Ace))
    deck.remove(Spades(CardValue.Two))
    deck.remove(Spades(CardValue.Three))
    deck.remove(Spades(CardValue.Queen))

   # deck.remove(Diamonds(CardValue.Ace))
   # deck.remove(Diamonds(CardValue.Queen))

    print(''.join(str(card) for card in deck.cards))

    print('test')

    print(diamond.numerical_value())
