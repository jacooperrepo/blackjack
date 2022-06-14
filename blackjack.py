"""Blackjack card game"""
from enum import Enum
from colorama import Fore, Style
from Pack.deck import Shoe, CardCollection


class PlayerHandStatus(Enum):
    InPlay: str = "InPlay"
    SplitInPlayHandOne: str = "SplitInPlayHandOne"
    SplitInPlayHandTwo: str = "SplitInPlayHandTwo"
    SplitEnded: str = "SplitEnded"
    Ended: str = "Ended"


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


class Blackjack:
    """Blackjack game class"""

    def __init__(self, shoe_size: int = 1):
        self.shoe_size = shoe_size
        self.shoe = Shoe(shoe_size)
        self.player_hand = [Hand(), Hand()]
        self.dealer_hand = Hand()
        self.player_status = PlayerHandStatus.InPlay
        self.in_game_message = ''

    def __str__(self):
        output = '\n' * 50
        output += Fore.GREEN + Style.BRIGHT + '------------------Blackjack------------------\n' \
                  + Style.RESET_ALL
        if self.player_status == PlayerHandStatus.Ended:
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Dealer ' + Style.RESET_ALL
        output += ' '.join(str(card) for card in self.dealer_hand.cards)
        output += "\n"
        if not self.player_status == PlayerHandStatus.Ended:
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Player ' + Style.RESET_ALL

        if self.player_status in (
        PlayerHandStatus.SplitInPlayHandOne, PlayerHandStatus.SplitInPlayHandTwo, PlayerHandStatus.SplitEnded):
            if self.player_status == PlayerHandStatus.SplitInPlayHandOne:
                output += Fore.BLACK + Style.BRIGHT + "." + Style.RESET_ALL
            output += ' '.join(str(card) for card in self.player_hand[0].cards)
            output += '|'
            if self.player_status == PlayerHandStatus.SplitInPlayHandTwo:
                output += Fore.BLACK + Style.BRIGHT + "." + Style.RESET_ALL
            output += ' '.join(str(card) for card in self.player_hand[1].cards)
        else:
            output += ' '.join(str(card) for card in self.player_hand[0].cards)

        output += Fore.GREEN + Style.BRIGHT + '\n---------------------------------------------\n' \
                  + Style.RESET_ALL
        output += 'remaining cards: {}'.format(self.shoe.remaining())
        output += '\n'
        output += self.in_game_message

        return output

    def reset(self) -> None:
        self.dealer_hand.reset()
        self.player_hand[0].reset()
        self.player_hand[1].reset()
        self.player_status = PlayerHandStatus.InPlay
        self.in_game_message = ''

    def play(self) -> None:
        """Game logic to run the game"""
        keep_playing = 'Y'

        try:
            while keep_playing.upper() == 'Y':
                self.dealer_hand.add(self.shoe.deal())
                self.player_hand[0].add(self.shoe.deal())

                self.process_input()

                keep_playing = input('Play another hand? Y or N ')

                self.reset()

        except IndexError:
            print(Fore.RED + Style.BRIGHT + 'Out of cards' + Style.RESET_ALL)

    def process_input(self) -> None:
        """Process player input"""
        entry = ''

        while entry.upper() != 'Q':
            print(self)

            entry = input('H to Hit S to Stand F to Fold | C Check Winner \n'
                          'R to Reset Deck X to Split ')

            if entry.upper() == 'H':  # Hit
                if not self.hit() and self.player_status is not PlayerHandStatus.SplitInPlayHandTwo:
                    print(self)
                    break
            elif entry.upper() == 'S':  # Stand
                if self.player_status == PlayerHandStatus.InPlay:
                    self.player_status = PlayerHandStatus.Ended
                elif self.player_status == PlayerHandStatus.SplitInPlayHandOne:
                    self.player_status = PlayerHandStatus.SplitInPlayHandTwo
                elif self.player_status == PlayerHandStatus.SplitInPlayHandTwo:
                    self.player_status = PlayerHandStatus.SplitEnded
            elif entry.upper() == 'C':  # Check Winner
                self.check_winner()
                print(self)
                break
            elif entry.upper() == 'F':  # Fold
                self.in_game_message = Fore.BLUE + Style.BRIGHT + 'Dealer wins!' + Style.RESET_ALL
                print(self)
                break
            elif entry.upper() == 'R':  # Reset deck
                self.shoe = Shoe(self.shoe_size)
            elif entry.upper() == 'X':  # Split
                if len(self.player_hand[0].cards) == 2:
                    if self.player_hand[0].cards[0].value == self.player_hand[0].cards[1].value:
                        self.player_status = PlayerHandStatus.SplitInPlayHandOne
                        self.player_hand[1].add(self.player_hand[0].cards[1])
                        self.player_hand[0].remove(self.player_hand[0].cards[1])

    def hit(self) -> bool:
        success = True

        if self.player_status == PlayerHandStatus.InPlay:
            self.player_hand[0].add(self.shoe.deal())
            if self.player_hand[0].is_bust():
                self.in_game_message = Fore.RED + Style.BRIGHT + 'Player Hand BUST! Dealer Wins!' \
                                       + Style.RESET_ALL
                success = False
        elif self.player_status == PlayerHandStatus.SplitInPlayHandOne:
            self.player_hand[0].add(self.shoe.deal())
            if self.player_hand[0].is_bust():
                self.in_game_message = Fore.RED + Style.BRIGHT + 'Player Hand BUST! Dealer Wins!' \
                                       + Style.RESET_ALL
                self.player_status = PlayerHandStatus.SplitInPlayHandTwo
                success = False
        elif self.player_status == PlayerHandStatus.SplitInPlayHandTwo:
            self.player_hand[1].add(self.shoe.deal())
            if self.player_hand[1].is_bust():
                self.in_game_message = Fore.RED + Style.BRIGHT + 'Player Split Hand BUST! Dealer Wins!' \
                                       + Style.RESET_ALL
                self.player_status = PlayerHandStatus.SplitEnded
                success = False
        else:
            self.dealer_hand.add(self.shoe.deal())
            if self.dealer_hand.is_bust():
                self.in_game_message = Fore.GREEN + Style.BRIGHT + 'Dealer BUST! Player Wins!' \
                                       + Style.RESET_ALL
                success = False

        return success

    @staticmethod
    def total_hand(cards: []) -> int:
        total = 0
        has_ace = False

        for card in cards:
            card_value = card.numerical_value()
            if card_value == 1:
                card_value = 11
                has_ace = True
            total += card_value

        if total > 21 and has_ace:
            total -= 10

        return total

    def winner_messaging(self, player_total: int, dealer_total: int, split_hand:bool = False):
        split_hand_text = ''

        if self.player_status in (PlayerHandStatus.SplitInPlayHandOne, PlayerHandStatus.SplitInPlayHandTwo,
                                  PlayerHandStatus.SplitEnded):
            if not split_hand:
                split_hand_text = " Hand 1"
            else:
                split_hand_text = " Hand 2"

        if dealer_total < player_total <= 21:
            self.in_game_message += Fore.GREEN + Style.BRIGHT + 'Player wins{}!\n'.format(
                split_hand_text) + Style.RESET_ALL
        elif player_total < dealer_total <= 21:
            self.in_game_message += Fore.BLUE + Style.BRIGHT + 'Dealer wins{}!\n'.format(split_hand_text) + Style.RESET_ALL
        elif player_total > 21:
            self.in_game_message += Fore.BLUE + Style.BRIGHT + 'Dealer wins{}!\n'.format(split_hand_text) + Style.RESET_ALL
        elif dealer_total > 21:
            self.in_game_message += Fore.GREEN + Style.BRIGHT + 'Player wins{}!\n'.format(
                split_hand_text) + Style.RESET_ALL
        else:
            self.in_game_message += Fore.BLACK + Style.BRIGHT + 'No winner{}\n'.format(split_hand_text) + Style.RESET_ALL

    def check_winner(self) -> None:
        """Check if player or dealer is the winner"""

        dealer_total = self.total_hand(self.dealer_hand.cards)
        player_total = self.total_hand(self.player_hand[0].cards)

        self.in_game_message = ''
        self.winner_messaging(player_total, dealer_total)

        if self.player_status in (PlayerHandStatus.SplitInPlayHandOne, PlayerHandStatus.SplitInPlayHandTwo,
                                  PlayerHandStatus.SplitEnded):
            self.winner_messaging(self.total_hand(self.player_hand[1].cards), dealer_total, True)


if __name__ == "__main__":
    game = Blackjack(1)
    game.play()
