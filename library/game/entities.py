from library.card.entities import CardCollection
from library.game.enums import PlayerHandStatus


class Hand(CardCollection):
    def __init__(self):
        super().__init__([])

    def is_bust(self) -> bool:
        total = 0

        for card in self.cards:
            total += card.numerical_value()

        if total > 21:
            return True

        return False


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