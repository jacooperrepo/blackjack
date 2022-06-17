"""Testing the deck of blackjack"""
import pytest
from library.card.entities import Shoe, Deck, Joker, Diamonds, Spades, Clubs, Hearts, CardValue, CardSuit, CardCollection


@pytest.fixture
def shoe():
    return Shoe(2)


@pytest.fixture
def player_deck():
    return Deck(False)


@pytest.fixture
def player_deck_with_joker():
    return Deck(True)


def test_deck_generation_number(player_deck):
    assert len(player_deck.cards) == 52


def test_deck_generation_number_with_joker(player_deck_with_joker):
    assert len(player_deck_with_joker.cards) == 53


def test_deck_generation_suits(player_deck):
    hearts = filter(lambda card: type(card) is Hearts, player_deck.cards)
    clubs = filter(lambda card: type(card) is Clubs, player_deck.cards)
    diamonds = filter(lambda card: type(card) is Diamonds, player_deck.cards)
    spades = filter(lambda card: type(card) is Spades, player_deck.cards)

    for card in player_deck.cards:
        if card is Hearts:
            break

    hearts_list = set(hearts)
    clubs_list = set(clubs)
    diamonds_list = set(diamonds)
    spades_list = set(spades)

    assert len(hearts_list) == 13
    assert len(clubs_list) == 13
    assert len(diamonds_list) == 13
    assert len(spades_list) == 13


def test_deck_generation_joker(player_deck_with_joker):
    joker = filter(lambda card: type(card) is Joker, player_deck_with_joker.cards)
    hearts = filter(lambda card: type(card) is Hearts, player_deck_with_joker.cards)
    clubs = filter(lambda card: type(card) is Clubs, player_deck_with_joker.cards)
    diamonds = filter(lambda card: type(card) is Diamonds, player_deck_with_joker.cards)
    spades = filter(lambda card: type(card) is Spades, player_deck_with_joker.cards)

    hearts_list = set(hearts)
    clubs_list = set(clubs)
    diamonds_list = set(diamonds)
    spades_list = set(spades)
    joker_list = set(joker)

    assert len(hearts_list) == 13
    assert len(clubs_list) == 13
    assert len(diamonds_list) == 13
    assert len(spades_list) == 13
    assert len(joker_list) == 1


def test_deal(player_deck):
    player_deck.deal()

    assert len(player_deck.cards) == 51


def test_deck_reset(player_deck):
    player_deck.deal()
    player_deck.reset()

    assert len(player_deck.cards) == 52


def test_card_numerical_value_ace():
    card = Diamonds(CardValue.ACE)

    assert card.numerical_value() == 1


def test_card_numerical_value_jack():
    card = Diamonds(CardValue.JACK)

    assert card.numerical_value() == 10


def test_card_numerical_value_queen():
    card = Diamonds(CardValue.QUEEN)

    assert card.numerical_value() == 10


def test_card_numerical_value_king():
    card = Diamonds(CardValue.KING)

    assert card.numerical_value() == 10


def test_card_numerical_value_joker():
    card = Joker()

    assert card.numerical_value() == 0


def test_add_card_to_deck(player_deck):
    player_deck.add(Diamonds(CardValue.ACE))

    found_cards = filter(lambda card: card.value == CardValue.ACE and card.suit == CardSuit.DIAMONDS, player_deck.cards)
    found_cards_list = list(found_cards)

    assert len(found_cards_list) == 2
    assert len(player_deck.cards) == 53


def test_remove_card_from_deck(player_deck):
    player_deck.remove(Spades(CardValue.ACE))

    found_cards = filter(lambda card: card.value == CardValue.ACE and card.suit == CardSuit.SPADES, player_deck.cards)
    found_cards_list = list(found_cards)

    assert len(found_cards_list) == 0
    assert len(player_deck.cards) == 51


@pytest.mark.parametrize("card1, card2, card3, expected", [
    (Diamonds(CardValue.ACE), Diamonds(CardValue.TEN), Diamonds(CardValue.TEN), True),
    (Spades(CardValue.ACE), Diamonds(CardValue.TEN), Diamonds(CardValue.THREE), False),
    (Diamonds(CardValue.ACE), Diamonds(CardValue.TEN), Clubs(CardValue.EIGHT), False),
    (Hearts(CardValue.ACE), Hearts(CardValue.TEN), Hearts(CardValue.TWO), True),
    (Clubs(CardValue.ACE), Clubs(CardValue.TEN), Clubs(CardValue.ACE), True)])
def test_card_collection_all_same_suite(card1, card2, card3, expected):
    cards = CardCollection([card1, card2, card3])
    assert cards.all_same_suit() == expected


@pytest.mark.parametrize("card1, card2, card3, expected", [
    (Diamonds(CardValue.ACE), Diamonds(CardValue.TEN), Diamonds(CardValue.SIX), [1, 10, 6]),
    (Spades(CardValue.ACE), Diamonds(CardValue.TEN), Diamonds(CardValue.FOUR), [1, 10, 4]),
    (Diamonds(CardValue.ACE), Diamonds(CardValue.TEN), Clubs(CardValue.FIVE), [1, 10, 5]),
    (Hearts(CardValue.ACE), Hearts(CardValue.TEN), Hearts(CardValue.SEVEN), [1, 10, 7]),
    (Clubs(CardValue.ACE), Clubs(CardValue.TEN), Clubs(CardValue.NINE), [1, 10, 9])])
def test_card_collection_values(card1, card2, card3, expected):
    cards = CardCollection([card1, card2, card3])
    assert cards.values() == expected


def test_shoe_creation(shoe):
    assert len(shoe.cards) == 104


def test_shoe_remaining(shoe):
    assert shoe.remaining() == 104


def test_shoe_deal(shoe):

    shoe.deal()
    assert shoe.remaining() == 103


def test_shoe_reset():
    shoe = Shoe(2)
    assert shoe.remaining() == 104

    shoe.deal()
    shoe.reset()
    assert len(shoe.cards) == 104
