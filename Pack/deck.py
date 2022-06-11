"""Playing deck and cards"""
from random import shuffle
from colorama import Fore, Style, init
from Pack.card_attributes import CardSuit, CardValue


class Card():
    """Generic card"""
    def __init__(self, value: CardValue, suit: CardSuit):
        self.suit = suit
        self.value = value

    def numerical_value(self) -> int:
        """Numerical value of card"""
        if self.value is CardValue.Joker:
            card_num_value = 0
        elif self.value is CardValue.Ace:
            card_num_value = 1
        elif self.value in(CardValue.Jack, CardValue.Queen, CardValue.King):
            card_num_value = 10
        else:
            card_num_value = int(self.value.value)
        return card_num_value


class Joker(Card):
    """Jocker card"""
    def __init__(self):
        super().__init__(CardValue.Joker, CardSuit.Joker)

    def __str__(self):
        return  f"{Fore.GREEN + Style.BRIGHT}🃏{self.value.value}" + Style.RESET_ALL


class Diamonds(Card):
    """Diamonds suit card"""
    def __init__(self, value: CardValue):
        super().__init__(value, CardSuit.Diamonds)

    def __str__(self):
        return  f"{Fore.RED + Style.BRIGHT}♦{self.value.value}" + Style.RESET_ALL


class Hearts(Card):
    """Hearts suit card"""
    def __init__(self, value: CardValue):
        super().__init__(value, CardSuit.Hearts)

    def __str__(self):
        return  f"{Fore.RED + Style.BRIGHT}♥{self.value.value}" + Style.RESET_ALL


class Clubs(Card):
    """Clubs suit card"""
    def __init__(self, value: CardValue):
        super().__init__(value, CardSuit.Clubs)

    def __str__(self):
        return  f"{Fore.BLACK + Style.BRIGHT}♣️{self.value.value}" + Style.RESET_ALL


class Spades(Card):
    """Spades suit card"""
    def __init__(self, value: CardValue):
        super().__init__(value, CardSuit.Spades)
    def __str__(self):
        return  f"{Fore.BLACK + Style.BRIGHT}♠{self.value.value}" + Style.RESET_ALL


class Deck():
    """Playing deck of cards"""
    def __init__(self, with_joker: bool = False):
        self.cards = self.generate_deck(with_joker)

    def shuffle(self):
        """Shuffle the deck"""
        shuffle(self.cards)

    def deal(self):
        """Deal one card from deck"""
        return self.cards.pop()

    def add(self, card: Card):
        """Add a card to the deck"""
        self.cards.append(card)

    def remove(self, card: Card):
        """Remove a card from the deck"""
        for remove_card in filter(lambda target: target.value == card.value and target.suit == card.suit, self.cards):
            self.cards.remove(remove_card)

    def reset(self, with_joker: bool = False):
        """Regenerate the deck of cards"""
        self.cards = self.generate_deck(with_joker)

    @staticmethod
    def generate_deck(with_joker: bool) -> list:
        """Generate new pack of 52 cards"""
        deck = []

        for value in filter(lambda card_value: card_value is not CardValue.Joker, CardValue):
            deck.append(Diamonds(value))
            deck.append(Clubs(value))
            deck.append(Hearts(value))
            deck.append(Spades(value))

        if with_joker:
            deck.append(Joker())

        return deck
