"""Playing deck and blackjack entities"""
from random import shuffle
from colorama import Fore, Style
from EventNotifier import Notifier

from src.card.enums import CardSuit, CardValue


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
        elif self.value in (CardValue.JACK, CardValue.QUEEN, CardValue.KING):
            card_num_value = 10
        else:
            card_num_value = int(self.value.value)
        return card_num_value


class Joker(Card):
    """Joker card"""

    def __init__(self):
        super().__init__(CardValue.JOKER, CardSuit.JOKER)

    def __str__(self):
        return f"{Fore.GREEN + Style.BRIGHT}🃏{self.value.value}" + Style.RESET_ALL


class Diamonds(Card):
    """Diamonds suit card"""

    def __init__(self, value):
        super().__init__(value, CardSuit.DIAMONDS)

    def __str__(self):
        return f"{Fore.RED + Style.BRIGHT}♦{self.value.value}" + Style.RESET_ALL


class Hearts(Card):
    """Hearts suit card"""

    def __init__(self, value):
        super().__init__(value, CardSuit.HEARTS)

    def __str__(self):
        return f"{Fore.RED + Style.BRIGHT}♥{self.value.value}" + Style.RESET_ALL


class Clubs(Card):
    """Clubs suit card"""

    def __init__(self, value):
        super().__init__(value, CardSuit.CLUBS)

    def __str__(self):
        return f"{Fore.BLACK + Style.BRIGHT}♣︎{self.value.value}" + Style.RESET_ALL


class Spades(Card):
    """Spades suit card"""

    def __init__(self, value):
        super().__init__(value, CardSuit.SPADES)

    def __str__(self):
        return f"{Fore.BLACK + Style.BRIGHT}♠{self.value.value}" + Style.RESET_ALL


class CardCollection:
    """Collection of blackjack and associated logic"""

    def __init__(self, cards: []):
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

    def remove(self, card: Card) -> bool:
        """Remove a card from the deck"""
        try:
            for remove_card in filter(lambda target: target.value == card.value \
                                                     and target.suit == card.suit, self.cards):
                self.cards.remove(remove_card)
        except ValueError:
            return False
        else:
            return True

    def total(self) -> int:
        """Total up card value in collection"""
        total = 0
        for card in self.cards:
            total += card.numerical_value()
        return total

    def remaining(self) -> int:
        """Return remaining blackjack in deck"""
        return len(self.cards)

    def reset(self) -> None:
        """Regenerate the deck of blackjack"""
        self.cards = []

    def has_card(self, *args) -> bool:
        """Remove a card from the deck"""
        card = None
        card_suit = None
        card_value = None

        exists = False

        for arg in args:
            if type(arg) == Card or issubclass(type(arg), Card):
                card = arg
                break
            elif type(arg) == CardSuit:
                card_suit = arg
            elif type(arg) == CardValue:
                card_value = arg

        if card is not None:
            exists = len(list(filter(lambda target: target.value == card.value \
                                    and target.suit == card.suit, self.cards))) > 0
        elif card_suit is not None and card_value is not None:
            exists = len(list(filter(lambda target: target.value == card_value \
                                     and target.suit == card_suit, self.cards))) > 0
        elif card_suit is not None:
            exists = len(list(filter(lambda target: target.suit == card_suit, self.cards))) > 0
        elif card_value is not None:
            exists = len(list(filter(lambda target: target.value == card_value, self.cards))) > 0

        return exists

    def all_same_suit(self) -> bool:
        """Returns True if all cards in collection are the same suit"""
        card_in_collection = len(self.cards)

        diamonds_count = len(list(filter(lambda target: target.suit == CardSuit.DIAMONDS, self.cards)))
        clubs_count = len(list(filter(lambda target: target.suit == CardSuit.CLUBS, self.cards)))
        spades_count = len(list(filter(lambda target: target.suit == CardSuit.SPADES, self.cards)))
        hearts_count = len(list(filter(lambda target: target.suit == CardSuit.HEARTS, self.cards)))

        if diamonds_count == card_in_collection or clubs_count == card_in_collection or \
                spades_count == card_in_collection or hearts_count == card_in_collection:
            return True

        return False

    def values(self) -> []:
        """Return a list of all card values"""
        values = []
        for card in self.cards:
            values.append(card.numerical_value())

        return values


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
    def generate_deck(with_joker: bool) -> []:
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


class Shoe(CardCollection):
    """A shoe containing multiple decks"""

    def __init__(self, size: int = 1):
        self.size = size
        super().__init__(self.generate_shoe())
        self.shuffle_cards()

        self.notifier = Notifier(["reset"])

    def reset(self) -> None:
        """Regenerate the deck of blackjack"""
        self.cards = self.generate_shoe()
        self.notifier.raise_event("reset")

    def generate_shoe(self) -> []:
        """Generate new shoe with specified number of decks"""
        shoe = []

        for deck in [Deck() for _ in range(0, self.size)]:
            shoe += deck.cards

        return shoe
