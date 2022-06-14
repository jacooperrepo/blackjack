"""Blackjack card game"""
from enum import Enum
from colorama import Fore, Style
from Pack.deck import Shoe, Card


class GameWinner(Enum):
    Player: str = "Player"
    Dealer: str = "Dealer"
    Draw: str = "Draw"


class HandStatus(Enum):
    Main: str = "Main"
    Split: str = "Split"
    SplitMainEnded = "SplitMainEnded"
    SplitEnd: str = "SplitEnd"
    End = "End"


class Hand:
    def __init__(self):
        self.status = HandStatus.Main
        self.cards_in_hand = {"hand": [], "split_hand": []}

    def cards(self):
        return self.cards_in_hand["hand"]

    def split_hand_cards(self):
        return self.cards_in_hand["split_hand"]

    def split(self):
        self.status = HandStatus.Split
        self.split_hand_cards().append(self.cards()[1])
        self.cards().pop()

    def reset(self):
        self.cards_in_hand = {"hand": [], "split_hand": []}
        self.status = HandStatus.Main

    def add_card(self, card: Card):
        if self.status == HandStatus.Main or self.status == HandStatus.Split:
            self.cards().append(card)
        elif self.status == HandStatus.SplitMainEnded:
            self.split_hand_cards().append(card)
        else:
            pass

    def total(self, split_hand:bool = False):
        total = 0

        if not split_hand:
            for card in self.cards():
                total += card.numerical_value()
        else:
            for card in self.split_hand_cards():
                total += card.numerical_value()

        return total

    def end_hand(self):
        if self.status == HandStatus.Main:
            self.status = HandStatus.End
        elif self.status == HandStatus.Split:
            self.status = HandStatus.SplitMainEnded
        elif self.status == HandStatus.SplitMainEnded:
            self.status = HandStatus.SplitEnd
        else:
            pass

    def is_bust(self, split_hand:bool = False) -> bool:
        total = 0
        if not split_hand:
            for card in self.cards():
                total += card.numerical_value()
        else:
            for card in self.split_hand_cards():
                total += card.numerical_value()

        if total > 21:
            return True

        return False


class Blackjack:
    """Blackjack game class"""

    def __init__(self, shoe_size:int = 1):
        self.shoe_size = shoe_size
        self.shoe = Shoe(shoe_size)
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def __str__(self):
        output = '\n'*50
        output += Fore.GREEN + Style.BRIGHT + '------------------Blackjack------------------\n' \
                  + Style.RESET_ALL
        if self.player_hand.status == HandStatus.End:
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Dealer ' + Style.RESET_ALL
        output += ' '.join(str(card) for card in self.dealer_hand.cards())
        output += "\n"
        if not self.player_hand.status == HandStatus.End:
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Player ' + Style.RESET_ALL

        if self.player_hand.status in(HandStatus.Split, HandStatus.SplitMainEnded, HandStatus.SplitEnd):
            output += ' '.join(str(card) for card in self.player_hand.cards())
            output += ' | '
            output += ' '.join(str(card) for card in self.player_hand.split_hand_cards())
        else:
            output += ' '.join(str(card) for card in self.player_hand.cards())

        output += Fore.GREEN + Style.BRIGHT + '\n---------------------------------------------\n' \
                  + Style.RESET_ALL
        output += 'remaining cards: {}'.format(self.shoe.remaining())
        output += '\n'
        return output

    def play(self) -> None:
        """Game logic to run the game"""
        keep_playing = 'Y'

        try:
            while keep_playing.upper() == 'Y':
                self.dealer_hand.add_card(self.shoe.deal())
                self.player_hand.add_card(self.shoe.deal())

                self.process_input()

                keep_playing = input('Play another hand? Y or N ')

                self.dealer_hand.reset()
                self.player_hand.reset()

        except IndexError:
            print(Fore.RED + Style.BRIGHT + 'Out of cards' + Style.RESET_ALL)

    def process_input(self) -> None:
        """Process player input"""
        entry = ''

        while entry.upper() != 'Q':
            print(self)
            entry = input('H to Hit S to Stand F to Fold | C Check Winner \n'
                          'R to Reset Deck X to Split ')

            if entry.upper() == 'H':
                if not self.hit():
                    break
            elif entry.upper() == 'S':
                self.player_hand.end_hand()
            elif entry.upper() == 'C':
                print(self)
                result = self.check_winner()
                if result == GameWinner.Player:
                    print(Fore.GREEN + Style.BRIGHT + 'Player wins!' + Style.RESET_ALL)
                elif result == GameWinner.Dealer:
                    print(Fore.BLUE + Style.BRIGHT + 'Dealer wins!' + Style.RESET_ALL)
                else:
                    print(Fore.BLACK + Style.BRIGHT + 'No winner' + Style.RESET_ALL)
                break
            elif entry.upper() == 'F':
                print(Fore.BLUE + Style.BRIGHT + 'Dealer wins!' + Style.RESET_ALL)
                break
            elif entry.upper() == 'R':
                self.shoe = Shoe(self.shoe_size)
            elif entry.upper() == 'X':
                self.player_hand.split()

    def hit(self) -> bool:
        success = True

        if self.player_hand.status in(HandStatus.End, HandStatus.SplitEnd):
            self.dealer_hand.add_card(self.shoe.deal())
            if self.dealer_hand.is_bust():
                print(self)
                print(Fore.GREEN + Style.BRIGHT + 'Dealer BUST! Player Wins!' \
                      + Style.RESET_ALL)
                success = False
        elif self.player_hand.status in(HandStatus.Main, HandStatus.Split):
            self.player_hand.add_card(self.shoe.deal())
            if self.player_hand.is_bust():
                print(self)
                print(Fore.RED + Style.BRIGHT + 'Player Hand BUST! Dealer Wins!' \
                      + Style.RESET_ALL)
                success = False
        elif self.player_hand.status == HandStatus.SplitMainEnded:
            self.player_hand.add_card(self.shoe.deal())
            if self.player_hand.is_bust(split_hand=True):
                print(self)
                print(Fore.RED + Style.BRIGHT + 'Player Split Hand BUST! Dealer Wins!' \
                      + Style.RESET_ALL)
                success = False

        return success

    def check_winner(self) -> str:
        """Check if player or dealer is the winner"""
        player_total = 0
        player_has_ace = False
        dealer_total = 0
        dealer_has_ace = False
        result = GameWinner.Draw

        for card in self.player_hand.cards():
            card_value = card.numerical_value()
            if card_value == 1:
                card_value = 11
                player_has_ace = True
            player_total += card_value

        if player_total > 21 and player_has_ace:
            player_total -= 10

        for card in self.dealer_hand.cards():
            card_value = card.numerical_value()
            if card_value == 1:
                card_value = 11
                dealer_has_ace = True
            dealer_total += card_value

        if dealer_total > 21 and dealer_has_ace:
            dealer_total -= 10

        if player_total > dealer_total and not self.player_hand.is_bust():
            result = GameWinner.Player
        elif dealer_total > player_total and not self.dealer_hand.is_bust():
            result = GameWinner.Dealer
        elif self.player_hand.is_bust():
            result = GameWinner.Dealer
        elif self.dealer_hand.is_bust():
            result = GameWinner.Player

        return result


if __name__ == "__main__":

    game = Blackjack(5)
    game.play()
