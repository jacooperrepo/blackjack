import pytest
from library.game.blackjack import Blackjack, Spanish21
from library.card.entities import Card
from library.card.enums import CardSuit, CardValue
from library.game.enums import PlayerHandStatus
from library.game.entities import Hand


@pytest.fixture(scope="class")
def blackjack_game():
    return Blackjack(1)


@pytest.mark.parametrize("card1, card2, card3, expected", [
    (Card(CardValue.KING, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), Card(CardValue.TWO, CardSuit.SPADES), False),
    (Card(CardValue.JACK, CardSuit.SPADES), Card(CardValue.TEN, CardSuit.SPADES), Card(CardValue.TWO, CardSuit.SPADES), True),
    (Card(CardValue.ACE, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), False),
    (Card(CardValue.SEVEN, CardSuit.SPADES), Card(CardValue.EIGHT, CardSuit.SPADES), Card(CardValue.SEVEN, CardSuit.SPADES), True),
    (Card(CardValue.SIX, CardSuit.SPADES), Card(CardValue.SEVEN, CardSuit.SPADES), Card(CardValue.EIGHT, CardSuit.SPADES), False)])
def test_check_bust(blackjack_game, card1, card2, card3, expected):
    blackjack_game.player.hand.reset()
    blackjack_game.player.hand.add(card1)
    blackjack_game.player.hand.add(card2)
    blackjack_game.player.hand.add(card3)

    assert blackjack_game.player.hand.bust() == expected


def test_reset(blackjack_game):
    blackjack_game.player.hand.add(Card(CardValue.SEVEN, CardSuit.CLUBS))
    blackjack_game.dealer.hand.add(Card(CardValue.SEVEN, CardSuit.CLUBS))
    blackjack_game.player.hand.reset()
    blackjack_game.dealer.hand.reset()

    assert len(blackjack_game.player.hand.cards) == 0
    assert len(blackjack_game.player.split_hand.cards) == 0
    assert len(blackjack_game.dealer.hand.cards) == 0
    assert blackjack_game.player.status == PlayerHandStatus.IN_PLAY


def test_check_print(blackjack_game):
    output = str(blackjack_game)

    assert output.index('Player') > 0
    assert output.index('Dealer') > 0
    assert output.index('remaining cards') > 0


@pytest.mark.parametrize("card1, card2, card3, expected", [
    (Card(CardValue.KING, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), Card(CardValue.TWO, CardSuit.SPADES), 0),
    (Card(CardValue.EIGHT, CardSuit.SPADES), Card(CardValue.TWO, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), -1),
    (Card(CardValue.ACE, CardSuit.SPADES), Card(CardValue.FIVE, CardSuit.SPADES), Card(CardValue.SIX, CardSuit.SPADES), 0),
    (Card(CardValue.SEVEN, CardSuit.SPADES), Card(CardValue.THREE, CardSuit.SPADES), Card(CardValue.TEN, CardSuit.SPADES), -1),
    (Card(CardValue.SIX, CardSuit.SPADES), Card(CardValue.TWO, CardSuit.SPADES), Card(CardValue.NINE, CardSuit.SPADES), -1)])
def test_check_player_winner(blackjack_game, card1, card2, card3, expected):
    blackjack_game.player.hand.reset()
    blackjack_game.dealer.hand.reset()

    blackjack_game.player.hand.add(card1)
    blackjack_game.player.hand.add(card2)
    blackjack_game.dealer.hand.add(card3)

    blackjack_game.check_winner()

    assert blackjack_game.in_game_message.find('Player wins') >= expected


@pytest.mark.parametrize("card1, card2, card3, expected", [
    (Card(CardValue.KING, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), 12),
    (Card(CardValue.ACE, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), 13),
    (Card(CardValue.JACK, CardSuit.SPADES), Card(CardValue.QUEEN, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), 21),
    (Card(CardValue.KING, CardSuit.SPADES), Card(CardValue.THREE, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), 14),
    (Card(CardValue.SIX, CardSuit.SPADES), Card(CardValue.TWO, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), 19)])
def test_total_hand(blackjack_game, card1, card2, card3, expected):
    blackjack_game.player.hand.add(card1)
    blackjack_game.player.hand.add(card2)
    blackjack_game.player.hand.add(card3)
    assert blackjack_game.player.hand.total() == expected


def test_hit(blackjack_game):
    blackjack_game.player.status = PlayerHandStatus.IN_PLAY
    blackjack_game.hit()
    assert len(blackjack_game.player.hand.cards) == 1
    assert len(blackjack_game.player.split_hand.cards) == 0

    blackjack_game.player.status = PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE
    blackjack_game.hit()
    assert len(blackjack_game.player.hand.cards) == 2
    assert len(blackjack_game.player.split_hand.cards) == 0

    blackjack_game.player.status = PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO
    blackjack_game.hit()
    assert len(blackjack_game.player.hand.cards) == 2
    assert len(blackjack_game.player.split_hand.cards) == 1

    blackjack_game.player.status = PlayerHandStatus.ENDED
    blackjack_game.hit()
    assert len(blackjack_game.player.hand.cards) == 2
    assert len(blackjack_game.player.split_hand.cards) == 1
    assert len(blackjack_game.dealer.hand.cards) == 1


@pytest.mark.parametrize("card1, card2, expected", [
    (Card(CardValue.KING, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), True),
    (Card(CardValue.TEN, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), True),
    (Card(CardValue.ACE, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), False),
    (Card(CardValue.THREE, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), False),
    (Card(CardValue.NINE, CardSuit.SPADES), Card(CardValue.ACE, CardSuit.SPADES), False)])
def test_blackjack_hand(card1, card2, expected):
    hand = Hand()
    hand.add(card1)
    hand.add(card2)
    assert hand.blackjack() == expected


def test_spanish_21_deck_creation():
    game = Spanish21(5)

    found_cards = filter(lambda card: card.value == CardValue.TEN, game.shoe.cards)

    assert len(game.shoe.cards) == 240
    assert len(list(found_cards)) == 0

    game.shoe.reset()

    found_cards = filter(lambda card: card.value == CardValue.TEN, game.shoe.cards)

    assert len(game.shoe.cards) == 240
    assert len(list(found_cards)) == 0