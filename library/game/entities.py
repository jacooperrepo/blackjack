from library.card.entities import CardCollection
from library.card.enums import CardValue
from library.game.enums import PlayerHandStatus


class Hand(CardCollection):
    def __init__(self):
        super().__init__([])

    def blackjack(self) -> bool:
        ace = False
        ten = False
        if len(self.cards) == 2:
            for card in self.cards:
                if card.value == CardValue.Ace:
                    ace = True
                elif card.numerical_value() == 10:
                    ten = True

        return ace and ten

    def bust(self) -> bool:
        if self.total() > 21:
            return True

        return False

    def total(self) -> int:
        total = 0
        ace_count = 0

        for card in self.cards:
            if card.value == CardValue.Ace:
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


class Player:
    def __init__(self):
        self.hand = Hand()


class BlackJackDealer(Player):
    def __init__(self):
        super().__init__()


class BlackJackPlayer(Player):
    def __init__(self, wallet_amount:float = 0):
        super().__init__()
        self.split_hand = Hand()
        self.status = PlayerHandStatus.InPlay
        self.wallet: float = wallet_amount