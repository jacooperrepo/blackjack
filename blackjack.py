from colorama import Fore, Style
from Pack.deck import Shoe


class Blackjack():
    _player_hand_end = False

    def __init__(self, shoe_size:int = 1):
        self.shoe_size = shoe_size
        self.shoe = Shoe(shoe_size)
        self.player_hand = []
        self.dealer_hand = []

    def __str__(self):
        output = ''
        output += Fore.GREEN + Style.BRIGHT + '------------------Blackjack------------------\n' + Style.RESET_ALL
        if self._player_hand_end:
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Dealer ' + Style.RESET_ALL
        output += ' '.join(str(card) for card in self.dealer_hand)
        output += "\n"
        if not self._player_hand_end:
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Player ' + Style.RESET_ALL

        output += ' '.join(str(card) for card in self.player_hand)
        output += Fore.GREEN + Style.BRIGHT + '\n---------------------------------------------\n' + Style.RESET_ALL
        output += 'remaining cards: {}'.format(self.shoe.remaining())
        output += '\n'
        return output

    def play(self) -> None:
        keep_playing = 'Y'

        try:
            while keep_playing.upper() == 'Y':
                entry = ''
                self.dealer_hand.append(self.shoe.deal())
                self.player_hand.append(self.shoe.deal())

                while entry.upper() != 'Q':
                    self.render_game_board()
                    entry = input('H to Hit S to Stand F to Fold | C Check Winner \n'
                                  'R to Reset Deck\n\n\n\n')

                    if entry.upper() == 'H':
                        if not self._player_hand_end:
                            self.player_hand.append(self.shoe.deal())
                            if self.check_bust(self.player_hand):
                                self.render_game_board()
                                print(Fore.RED + Style.BRIGHT + 'Player BUST! Dealer Wins!\n\n\n\n\n' + Style.RESET_ALL)
                                break
                        else:
                            self.dealer_hand.append(self.shoe.deal())
                            if self.check_bust(self.dealer_hand):
                                self.render_game_board()
                                print(Fore.GREEN + Style.BRIGHT + 'Dealer BUST! Player Wins!\n\n\n\n\n' + Style.RESET_ALL)
                                break
                    elif entry.upper() == 'S':
                        self._player_hand_end = True
                    elif entry.upper() == 'C':
                        self.check_winner()
                        break
                    elif entry.upper() == 'F':
                        print(Fore.BLUE + Style.BRIGHT + 'Dealer wins!' + Style.RESET_ALL)
                        break
                    elif entry.upper() == 'R':
                        self.shoe = Shoe(self.shoe_size)
                        continue

                keep_playing = input('Play another hand? Y or N ')
                self.reset_hands()
        except IndexError:
            print(Fore.RED + Style.BRIGHT + 'Out of cards' + Style.RESET_ALL)


    @staticmethod
    def check_bust(cards: list) -> bool:
        total = 0
        for card in cards:
            total += card.numerical_value()

        if total > 21:
            return True

        return False

    def reset_hands(self):
        self.player_hand = []
        self.dealer_hand = []
        self._player_hand_end = False

    def check_winner(self) -> None:
        player_total = 0
        player_has_ace = False
        dealer_total = 0
        dealer_has_ace = False

        for card in self.player_hand:
            card_value = card.numerical_value()
            if card_value == 1:
                card_value = 11
                player_has_ace = True
            player_total += card_value

        if player_total > 21 and player_has_ace:
            player_total -= 10

        for card in self.dealer_hand:
            card_value = card.numerical_value()
            if card_value == 1:
                card_value = 11
                dealer_has_ace = True
            dealer_total += card_value

        if dealer_total > 21 and dealer_has_ace:
            dealer_total -= 10

        player_bust = player_total > 21
        dealer_bust = dealer_total > 21

        if player_total > dealer_total and not player_bust:
            print(Fore.GREEN + Style.BRIGHT + 'Player wins!' + Style.RESET_ALL)
        elif dealer_total > player_total and not dealer_bust:
            print(Fore.BLUE + Style.BRIGHT + 'Dealer wins!' + Style.RESET_ALL)
        else:
            print(Fore.BLACK + Style.BRIGHT + 'No winner' + Style.RESET_ALL)

    def render_game_board(self) -> None:
        print('\n'*50)
        print(self)


if __name__ == "__main__":

    game = Blackjack(1)
    game.play()


