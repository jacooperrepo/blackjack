import pytest
from src.game.blackjack import Blackjack, Spanish21, FaceUp21
from src.card.entities import Card, Diamonds, Spades, Hearts, Clubs
from src.card.enums import CardSuit, CardValue
from src.game.enums import PlayerHandStatus, GameWinner
from src.game.entities import Hand


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


@pytest.mark.parametrize("card1, card2, card3, card4, expected", [
    (Diamonds(CardValue.TEN), Clubs(CardValue.ACE), Spades(CardValue.KING), Hearts(CardValue.JACK), GameWinner.PLAYER),
    (Diamonds(CardValue.TEN), Clubs(CardValue.QUEEN), Spades(CardValue.KING), Hearts(CardValue.JACK), GameWinner.DRAW),
    (Diamonds(CardValue.TEN), Clubs(CardValue.THREE), Spades(CardValue.SEVEN), Hearts(CardValue.EIGHT), GameWinner.DEALER),
    (Diamonds(CardValue.ACE), Clubs(CardValue.ACE), Spades(CardValue.NINE), Hearts(CardValue.TWO), GameWinner.PLAYER),
    (Diamonds(CardValue.KING), Clubs(CardValue.ACE), Spades(CardValue.KING), Hearts(CardValue.QUEEN), GameWinner.PLAYER)])
def test_check_player_winner(blackjack_game, card1, card2, card3, card4, expected):
    blackjack_game.player.hand.reset()
    blackjack_game.dealer.hand.reset()

    blackjack_game.player.hand.add(card1)
    blackjack_game.player.hand.add(card2)
    blackjack_game.dealer.hand.add(card3)
    blackjack_game.dealer.hand.add(card4)

    blackjack_game.check_winner()

    assert blackjack_game.player.hand.outcome == expected
    assert blackjack_game.dealer.hand.outcome == GameWinner.NOTSET


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


@pytest.mark.parametrize("card1, card2, status, expected", [
    (Spades(CardValue.KING), Spades(CardValue.KING), PlayerHandStatus.IN_PLAY, 10),
    (Spades(CardValue.KING), Spades(CardValue.QUEEN), PlayerHandStatus.IN_PLAY, 10),
    (Hearts(CardValue.ACE), Spades(CardValue.ACE), PlayerHandStatus.IN_PLAY, 10),
    (Clubs(CardValue.TEN), Spades(CardValue.TEN), PlayerHandStatus.IN_PLAY, 10),
    (Clubs(CardValue.TEN), Spades(CardValue.NINE), PlayerHandStatus.IN_PLAY, 10),
    (Diamonds(CardValue.NINE), Spades(CardValue.NINE), PlayerHandStatus.IN_PLAY, 10),
    (Spades(CardValue.EIGHT), Spades(CardValue.EIGHT), PlayerHandStatus.IN_PLAY, 10),
    (Spades(CardValue.SIX), Spades(CardValue.SIX), PlayerHandStatus.IN_PLAY, 10),
    (Spades(CardValue.JACK), Spades(CardValue.TEN), PlayerHandStatus.IN_PLAY, 10),
    (Spades(CardValue.FIVE), Spades(CardValue.FOUR), PlayerHandStatus.IN_PLAY, 20),
    (Spades(CardValue.ACE), Spades(CardValue.TEN), PlayerHandStatus.IN_PLAY, 10),
    (Spades(CardValue.FIVE), Spades(CardValue.FIVE), PlayerHandStatus.IN_PLAY, 20),
    (Spades(CardValue.THREE), Spades(CardValue.NINE), PlayerHandStatus.IN_PLAY, 10),
    (Spades(CardValue.FOUR), Spades(CardValue.FOUR), PlayerHandStatus.IN_PLAY, 10)])
def test_faceup_21_double_down(card1, card2, status, expected):
    game = FaceUp21(1, 0)

    game.player.hand.add(card1)
    game.player.hand.add(card2)
    game.player.status = status
    game.player.hand.bet = 10
    game.player.wallet = 10
    game.double_down()

    assert game.player.hand.bet == expected


def test_faceup_21_calculate_winnings():
    game = FaceUp21(1, 0)

    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.TEN, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.TEN, CardSuit.SPADES))

    # dealer blackjack beats a player blackjack
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 0

    game.reset()
    game.player.wallet = 0

    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.TEN, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.TWO, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.TEN, CardSuit.SPADES))

    # dealer blackjack beats a player blackjack
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 20

    game.reset()
    game.player.wallet = 0

    game.player.hand.add(Card(CardValue.TWO, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.TEN, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.TWO, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.TEN, CardSuit.SPADES))

    # dealer blackjack beats a player blackjack
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 10


def test_spanish_21_calculate_winnings():
    game = Spanish21(1, 0)

    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.TEN, CardSuit.SPADES))

    # Blackjack pays 3/2
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 15

    game.reset()
    game.player.wallet = 0

    # A five-card 21 pays out at 3:2
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.TEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.EIGHT, CardSuit.SPADES))
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 15

    game.reset()
    game.player.wallet = 0

    # A Six-card 21 pays 2:1
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.TEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 20

    game.reset()
    game.player.wallet = 0

    # A seven-card 21 pays out at 3:1
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.THREE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 30

    game.reset()
    game.player.wallet = 0

    # A 678 of mixed suit pays 3:2
    game.player.hand.add(Card(CardValue.SIX, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.DIAMONDS))
    game.player.hand.add(Card(CardValue.EIGHT, CardSuit.SPADES))
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 15

    game.reset()
    game.player.wallet = 0

    # A 678 same suit it pays 2:1
    game.player.hand.add(Card(CardValue.SIX, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.EIGHT, CardSuit.SPADES))
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 20

    game.reset()
    game.player.wallet = 0

    # A 777 of mixed suit pays 3:2
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.DIAMONDS))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 15

    game.reset()
    game.player.wallet = 0

    # A 777 of same suit it pays 2:1
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 20

    game.reset()
    game.player.wallet = 0

    # A 777 of same suit it pays 2:1
    # If a player has 777 of the same suit and the dealer is holding a 7 in any suit,
    # there is a $1,000 bonus paid to the player.
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.SEVEN, CardSuit.DIAMONDS))

    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 1020

    game.reset()
    game.player.wallet = 0

    # A 777 of same suit it pays 2:1
    # If the player has bet more than $25 at the start of the hand, this climbs all the way to $5,000.
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.SEVEN, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.SEVEN, CardSuit.DIAMONDS))
    game.player.hand.bet = 26
    game.check_winner()
    assert game.player.wallet == 5052

    game.reset()
    game.player.wallet = 0

    # Blackjack always wins, and is always paid 3:2 regardless of whether or not the dealer has a blackjack.
    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.TEN, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.JACK, CardSuit.DIAMONDS))
    game.player.hand.bet = 10
    game.check_winner()
    assert game.player.wallet == 15


def test_spanish_21_player_blackjack_always_wins():
    game = Spanish21(1, 0)
    game.player.wallet = 0

    game.player.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.player.hand.add(Card(CardValue.TEN, CardSuit.SPADES))

    game.dealer.hand.add(Card(CardValue.ACE, CardSuit.SPADES))
    game.dealer.hand.add(Card(CardValue.TEN, CardSuit.SPADES))

    # Blackjack pays 3/2
    game.player.hand.bet = 10
    game.check_winner()

    assert game.player.wallet == 15


def add_cards(blackjack_game):
    blackjack_game.player.hand.bet = 10
    blackjack_game.dealer.hand.add(blackjack_game.shoe.deal())
    blackjack_game.player.hand.add(blackjack_game.shoe.deal())
    blackjack_game.player.hand.add(blackjack_game.shoe.deal())

