"""Entities for the blackjack game"""
from src.card.entities import CardCollection
from src.card.enums import CardValue
from src.game.enums import PlayerHandStatus, GameWinner


class Hand(CardCollection):
    """Collection of blackjack for a hand in a card game"""
    def __init__(self):
        super().__init__([])
        self.bet:float = 0
        self.double_down:bool = False
        self.outcome = GameWinner.NOTSET

    def __str__(self):
        return ' '.join(str(card) for card in self.cards)

    def blackjack(self) -> bool:
        """Return True or False if the hand is blackjack"""
        ace = False
        ten = False
        if len(self.cards) == 2:
            for card in self.cards:
                if card.value == CardValue.ACE:
                    ace = True
                elif card.numerical_value() == 10:
                    ten = True

        return ace and ten

    def bust(self) -> bool:
        """Return True or False if hand is bust"""
        if self.total() > 21:
            return True

        return False

    def total(self) -> int:
        """Return total of hand. Note. Aces are considered 11 unless total exceeds 21"""
        total = 0
        ace_count = 0

        for card in self.cards:
            if card.value == CardValue.ACE:
                ace_count += 1
                total += 11
            else:
                total += card.numerical_value()

        if total > 21 and ace_count > 0:
            for _ in range(0, ace_count):
                if total <= 21:
                    break

                total -= 10

        return total

    def reset(self) -> None:
        """Regenerate the deck of blackjack"""
        super().reset()
        self.bet = 0
        self.double_down = False


class Player:
    """Generic player class"""
    def __init__(self):
        self.hand = Hand()

    def reset(self) -> None:
        self.hand.reset()

    def __str__(self):
        return ' '.join(str(card) for card in self.hand.cards)


class BlackJackPlayer(Player):
    """Blackjack player"""
    def __init__(self, wallet_amount:float = 0):
        super().__init__()

        self.split_hand = Hand()
        self.status = PlayerHandStatus.IN_PLAY
        self.wallet: float = wallet_amount

    def reset(self) -> None:
        super().reset()
        self.split_hand.reset()
        self.status = PlayerHandStatus.IN_PLAY


class BlackJackDealer(Player):
    """Blackjack player"""
    def __init__(self):
        super().__init__()

        self.hand_visible = False

    def __str__(self):
        if self.hand_visible:
            return super().__str__()
        elif len(self.hand.cards) == 2:
            return str(self.hand.cards[0]) + ' ##'
        else:
            return ''

    def reset(self) -> None:
        super().reset()
        self.hand_visible = False
