import pytest
from blackjack import Blackjack, PlayerHandStatus
from Pack.deck import Card, Spades
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
    blackjack_game.player.hand.reset()
    blackjack_game.player.hand.add(card1)
    blackjack_game.player.hand.add(card2)
    blackjack_game.player.hand.add(card3)

    assert blackjack_game.player.hand.is_bust() == expected


def test_reset(blackjack_game):
    blackjack_game.player.hand.add(Card(CardValue.Seven, CardSuit.Clubs))
    blackjack_game.dealer.hand.add(Card(CardValue.Seven, CardSuit.Clubs))
    blackjack_game.player.hand.reset()
    blackjack_game.dealer.hand.reset()

    assert len(blackjack_game.player.hand.cards) == 0
    assert len(blackjack_game.player.split_hand.cards) == 0
    assert len(blackjack_game.dealer.hand.cards) == 0
    assert blackjack_game.player.status == PlayerHandStatus.InPlay


def test_check_print(blackjack_game):
    output = str(blackjack_game)

    assert output.index('Player') > 0
    assert output.index('Dealer') > 0
    assert output.index('remaining cards') > 0


@pytest.mark.parametrize("card1, card2, card3, expected", [
    (Card(CardValue.King, CardSuit.Spades), Card(CardValue.Ace, CardSuit.Spades), Card(CardValue.Two, CardSuit.Spades), 0),
    (Card(CardValue.Eight, CardSuit.Spades), Card(CardValue.Two, CardSuit.Spades), Card(CardValue.Ace, CardSuit.Spades), -1),
    (Card(CardValue.Ace, CardSuit.Spades), Card(CardValue.Five, CardSuit.Spades), Card(CardValue.Six, CardSuit.Spades), 0),
    (Card(CardValue.Seven, CardSuit.Spades), Card(CardValue.Three, CardSuit.Spades), Card(CardValue.Ten, CardSuit.Spades), -1),
    (Card(CardValue.Six, CardSuit.Spades), Card(CardValue.Two, CardSuit.Spades), Card(CardValue.Nine, CardSuit.Spades), -1)])
def test_check_player_winner(blackjack_game, card1, card2, card3, expected):
    blackjack_game.player.hand.reset()
    blackjack_game.dealer.hand.reset()

    blackjack_game.player.hand.add(card1)
    blackjack_game.player.hand.add(card2)
    blackjack_game.dealer.hand.add(card3)

    blackjack_game.check_winner()

    assert blackjack_game.in_game_message.find('Player wins') >= expected


@pytest.mark.parametrize("card1, card2, expected", [
    (Card(CardValue.King, CardSuit.Spades), Card(CardValue.Ace, CardSuit.Spades), 21),
    (Card(CardValue.Ace, CardSuit.Spades), Card(CardValue.Ace, CardSuit.Spades), 12),
    (Card(CardValue.Jack, CardSuit.Spades), Card(CardValue.Queen, CardSuit.Spades), 20),
    (Card(CardValue.King, CardSuit.Spades), Card(CardValue.Three, CardSuit.Spades), 13),
    (Card(CardValue.Six, CardSuit.Spades), Card(CardValue.Two, CardSuit.Spades), 8)])
def test_total_hand(blackjack_game, card1, card2, expected):
    assert blackjack_game.total_hand([card1, card2]) == expected


def test_hit(blackjack_game):
    blackjack_game.player.status = PlayerHandStatus.InPlay
    blackjack_game.hit()
    assert len(blackjack_game.player.hand.cards) == 1

    blackjack_game.player.status = PlayerHandStatus.SplitInPlayHandOne
    blackjack_game.hit()
    assert len(blackjack_game.player.hand.cards) == 2

    blackjack_game.player.status = PlayerHandStatus.SplitInPlayHandTwo
    blackjack_game.hit()
    assert len(blackjack_game.player.hand.cards) == 2
    assert len(blackjack_game.player.split_hand.cards) == 1

    blackjack_game.player.status = PlayerHandStatus.Ended
    blackjack_game.hit()
    assert len(blackjack_game.player.hand.cards) == 2
    assert len(blackjack_game.player.split_hand.cards) == 1
    assert len(blackjack_game.dealer.hand.cards) == 1

