import pytest
from blackjack import Blackjack
from Pack.deck import Card
from Pack.card_attributes import CardSuit, CardValue


@pytest.fixture(scope="class")
def blackjack_game():
    return Blackjack(1)


@pytest.mark.parametrize("card1, card2, card3, expected", [
    (Card(CardValue.King, CardSuit.Spades), Card(CardValue.Ace, CardSuit.Spades), Card(CardValue.Two, CardSuit.Spades), False),
    (Card(CardValue.Jack, CardSuit.Spades), Card(CardValue.Ten, CardSuit.Spades), Card(CardValue.Two, CardSuit.Spades), True),
    (Card(CardValue.Ace, CardSuit.Spades), Card(CardValue.Ace, CardSuit.Spades), Card(CardValue.Ace, CardSuit.Spades), False),
    (Card(CardValue.Seven, CardSuit.Spades), Card(CardValue.Eight, CardSuit.Spades), Card(CardValue.Seven, CardSuit.Spades), True),
    (Card(CardValue.Six, CardSuit.Spades), Card(CardValue.Seven, CardSuit.Spades), Card(CardValue.Eight, CardSuit.Spades), False)])
def test_check_bust(blackjack_game, card1, card2, card3, expected):
    assert blackjack_game.check_bust([card1, card2, card3]) is expected


def test_reset(blackjack_game):
    blackjack_game.player_hand.append(Card(CardValue.Seven, CardSuit.Clubs))
    blackjack_game.dealer_hand.append(Card(CardValue.Seven, CardSuit.Clubs))
    blackjack_game.reset_hands()

    assert len(blackjack_game.player_hand) == 0
    assert len(blackjack_game.dealer_hand) == 0


def test_check_print(blackjack_game):
    output = str(blackjack_game)

    assert output.index('Player') > 0
    assert output.index('Dealer') > 0
    assert output.index('remaining cards') > 0


