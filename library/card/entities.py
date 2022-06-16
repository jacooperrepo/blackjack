"""Playing deck and blackjack entities"""
from random import shuffle
from colorama import Fore, Style
from library.card.enums import CardSuit, CardValue


class Card:
    """Generic card"""
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value

    def numerical_value(self) -> int:
        """Numerical value of card"""
        if self.value is CardValue.JOKER:
            card_num_value = 0
        elif self.value is CardValue.ACE:
            card_num_value = 1
        elif self.value in(CardValue.JACK, CardValue.QUEEN, CardValue.KING):
            card_num_value = 10
        else:
            card_num_value = int(self.value.value)
        return card_num_value


class Joker(Card):
    """Joker card"""
    def __init__(self):
        super().__init__(CardValue.JOKER, CardSuit.JOKER)

    def __str__(self):
        return  f"{Fore.GREEN + Style.BRIGHT}🃏{self.value.value}" + Style.RESET_ALL


class Diamonds(Card):
    """Diamonds suit card"""
    def __init__(self, value):
        super().__init__(value, CardSuit.DIAMONDS)

    def __str__(self):
        return  f"{Fore.RED + Style.BRIGHT}♦{self.value.value}" + Style.RESET_ALL


class Hearts(Card):
    """Hearts suit card"""
    def __init__(self, value):
        super().__init__(value, CardSuit.HEARTS)

    def __str__(self):
        return  f"{Fore.RED + Style.BRIGHT}♥{self.value.value}" + Style.RESET_ALL


class Clubs(Card):
    """Clubs suit card"""
    def __init__(self, value):
        super().__init__(value, CardSuit.CLUBS)

    def __str__(self):
        return  f"{Fore.BLACK + Style.BRIGHT}♣︎{self.value.value}" + Style.RESET_ALL


class Spades(Card):
    """Spades suit card"""
    def __init__(self, value):
        super().__init__(value, CardSuit.SPADES)

    def __str__(self):
        return  f"{Fore.BLACK + Style.BRIGHT}♠{self.value.value}" + Style.RESET_ALL


class CardCollection:
    """Collection of blackjack and associated logic"""
    def __init__(self, cards:[]):
        self.cards = cards

    def shuffle_cards(self) -> None:
        """Shuffle the deck"""
        shuffle(self.cards)

    def deal(self) -> Card:
        """Deal one card from deck"""
        return self.cards.pop()

    def add(self, card: Card) -> None:
        """Add a card to the deck"""
        self.cards.append(card)

    def remove(self, card: Card) -> None:
        """Remove a card from the deck"""
        for remove_card in filter(lambda target: target.value == card.value \
                                  and target.suit == card.suit, self.cards):
            self.cards.remove(remove_card)

    def total(self) -> int:
        """Total up blackjack in collection"""
        total = 0
        for card in self.cards:
            total += card.numerical_value()
        return total

    def reset(self) -> None:
        """Regenerate the deck of blackjack"""
        self.cards = []


class Deck(CardCollection):
    """Playing deck of blackjack"""
    def __init__(self, with_joker: bool = False, shuffle_cards: bool = False):
        super().__init__(self.generate_deck(with_joker))

        self.has_joker = with_joker
        if shuffle_cards:
            self.shuffle_cards()

    def reset(self) -> None:
        """Regenerate the deck of blackjack"""
        self.cards = self.generate_deck(self.has_joker)

    @staticmethod
    def generate_deck(with_joker: bool) -> list:
        """Generate new pack of 52 blackjack"""
        deck = []

        for value in filter(lambda card_value: card_value is not CardValue.JOKER, CardValue):
            deck.append(Diamonds(value))
            deck.append(Clubs(value))
            deck.append(Hearts(value))
            deck.append(Spades(value))

        if with_joker:
            deck.append(Joker())

        return deck


class Shoe:
    """A shoe containing multiple decks"""

    def __init__(self, size:int = 1):
        self.cards = []
        self.size = size
        self.generate_shoe()

    def generate_shoe(self):
        """Generate new shoe with specified number of decks"""
        shoe = []

        for _ in range(0, self.size):
            for card in Deck().cards:
                shoe.append(card)

        shuffle(shoe)
        self.cards = shoe

    def deal(self) -> Card:
        """Deal one card from the shoe"""
        return self.cards.pop()

    def remaining(self) -> int:
        """Return remaining blackjack in shoe"""
        return len(self.cards)

    def reset(self, size: int = 1):
        """Reset shoe to desired deck count"""
        self.size = size
        self.generate_shoe()
