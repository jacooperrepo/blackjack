from enum import Enum


class GameWinner(Enum):
    NotSet: str = "NotSet"
    Player: str = "Player"
    Dealer: str = "Dealer"
    Draw: str = "Draw"


class PlayerHandStatus(Enum):
    InPlay: str = "InPlay"
    SplitInPlayHandOne: str = "SplitInPlayHandOne"
    SplitInPlayHandTwo: str = "SplitInPlayHandTwo"
    SplitEnded: str = "SplitEnded"
    Ended: str = "Ended"


