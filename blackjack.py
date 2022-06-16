"""Blackjack card game"""
from colorama import Fore, Style
from library.card.entities import Shoe
from library.game.entities import BlackJackPlayer, BlackJackDealer
from library.game.enums import GameWinner, PlayerHandStatus
from library.exceptions.game import OutOfFundsException


class Blackjack:
    """Blackjack game class"""

    def __init__(self, shoe_size: int = 1, wallet_amount:float = 100):
        self.shoe_size = shoe_size
        self.shoe = Shoe(shoe_size)
        self.player = BlackJackPlayer()
        self.player.wallet = wallet_amount
        self.bet:float = 0
        self.split_bet:float = 0
        self.dealer = BlackJackDealer()
        self.in_game_message = ''

    def __str__(self):
        output = '\n' * 50
        output += Fore.LIGHTRED_EX + Style.NORMAL + "bet: $" + str(round(self.bet, 2)) + "\n"
        if self.split_bet > 0:
            output += Fore.LIGHTRED_EX + Style.NORMAL + "split bet: $" + str(round(self.split_bet, 2)) + "\n"
        output += Fore.GREEN + Style.BRIGHT + '------------------Blackjack------------------\n' \
                  + Style.RESET_ALL
        if self.player.status in(PlayerHandStatus.Ended, PlayerHandStatus.SplitEnded):
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Dealer ' + Style.RESET_ALL
        output += ' '.join(str(card) for card in self.dealer.hand.cards)
        output += "\n"
        if not self.player.status in(PlayerHandStatus.Ended, PlayerHandStatus.SplitEnded):
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Player ' + Style.RESET_ALL

        if self.player.status in (PlayerHandStatus.SplitInPlayHandOne,
                                  PlayerHandStatus.SplitInPlayHandTwo, PlayerHandStatus.SplitEnded):
            if self.player.status == PlayerHandStatus.SplitInPlayHandOne:
                output += Fore.BLACK + Style.BRIGHT + "." + Style.RESET_ALL
            output += ' '.join(str(card) for card in self.player.hand.cards)
            output += '|'
            if self.player.status == PlayerHandStatus.SplitInPlayHandTwo:
                output += Fore.BLACK + Style.BRIGHT + "." + Style.RESET_ALL
            output += ' '.join(str(card) for card in self.player.split_hand.cards)
        else:
            output += ' '.join(str(card) for card in self.player.hand.cards)

        output += Fore.GREEN + Style.BRIGHT + '\n---------------------------------------------\n' \
                  + Style.RESET_ALL
        output += 'remaining cards: {}'.format(self.shoe.remaining())
        output += '\n'
        output += Fore.BLACK + Style.RESET_ALL + "wallet: $" + str(round(self.player.wallet, 2)) + "\n"
        output += self.in_game_message

        return output

    def reset(self) -> None:
        """Reset game and hands"""
        self.dealer.hand.reset()
        self.player.hand.reset()
        self.player.split_hand.reset()
        self.player.status = PlayerHandStatus.InPlay
        self.bet = 0
        self.split_bet = 0

    def play(self) -> None:
        """Game logic to run the game"""
        keep_playing = ''

        try:
            while keep_playing != 'Q':
                self.dealer.hand.add(self.shoe.deal())
                self.player.hand.add(self.shoe.deal())

                keep_playing = self.process_input()
                print(self)

                self.reset()

        except IndexError:
            print(Fore.RED + Style.BRIGHT + 'Out of cards' + Style.RESET_ALL)
        except OutOfFundsException:
            print(Fore.RED + Style.BRIGHT + 'Out of funds' + Style.RESET_ALL)

    def place_your_bets(self):
        """Get bet input from user"""
        valid_entry = False
        valid_bet:float = 0

        while not valid_entry:
            if self.player.wallet <= 0:
                raise OutOfFundsException

            bet = input('Place your bet: ')

            try:
                if bet.isdigit():
                    valid_bet = float(bet)
                else:
                    continue
            except ValueError:
                pass
            else:
                valid_entry = True

        if self.player.wallet - valid_bet < 0:
            self.place_your_bets()
        else:
            self.player.wallet -= valid_bet
            self.bet = valid_bet

    def process_input(self) -> str:
        """Process player input"""
        entry = ''

        while entry.upper() != 'Q':
            print(self)

            if entry == '':
                self.place_your_bets()
                self.in_game_message = ''

            print(self)

            entry = input('{}H {}to hit {}S {}to stand {}F {}to fold\n'
                          '{}R {}to reset deck {}X {}to split {}Q {}to end '
                          .format(Fore.LIGHTBLUE_EX,
                                  Fore.LIGHTBLACK_EX,
                                  Fore.LIGHTBLUE_EX,
                                  Fore.LIGHTBLACK_EX,
                                  Fore.LIGHTBLUE_EX,
                                  Fore.LIGHTBLACK_EX,
                                  Fore.LIGHTBLUE_EX,
                                  Fore.LIGHTBLACK_EX,
                                  Fore.LIGHTBLUE_EX,
                                  Fore.LIGHTBLACK_EX,
                                  Fore.LIGHTBLUE_EX,
                                  Fore.LIGHTBLACK_EX
                                  ))

            self.in_game_message = ''

            if entry.upper() == 'H':  # Hit
                if not self.hit() and self.player.status is not PlayerHandStatus.SplitInPlayHandTwo:
                    self.check_winner()
                    break
            elif entry.upper() == 'S':  # Stand
                if self.player.status in(PlayerHandStatus.Ended, PlayerHandStatus.SplitEnded):
                    self.check_winner()
                    break
                elif self.player.status == PlayerHandStatus.InPlay:
                    self.player.status = PlayerHandStatus.Ended
                elif self.player.status == PlayerHandStatus.SplitInPlayHandOne:
                    self.player.status = PlayerHandStatus.SplitInPlayHandTwo
                elif self.player.status == PlayerHandStatus.SplitInPlayHandTwo:
                    self.player.status = PlayerHandStatus.SplitEnded
            elif entry.upper() == 'F':  # Fold
                self.in_game_message = Fore.BLUE + Style.BRIGHT + 'Dealer wins!' + Style.RESET_ALL
                break
            elif entry.upper() == 'R':  # Reset deck
                self.shoe = Shoe(self.shoe_size)
            elif entry.upper() == 'X':  # Split
                if len(self.player.hand.cards) == 2:
                    if self.player.hand.cards[0].value == self.player.hand.cards[1].value:
                        # Split bet if funds allow
                        if self.player.wallet - self.bet >= 0:
                            self.player.status = PlayerHandStatus.SplitInPlayHandOne
                            self.player.split_hand.add(self.player.hand.cards[1])
                            self.player.hand.remove(self.player.hand.cards[1])

                            self.split_bet = self.bet
                            self.player.wallet -= self.bet
                        else:
                            # Not enough funds to split hand
                            pass

        return entry.upper()

    def hit(self) -> bool:
        """Draw card and assign to hand"""
        success = True

        if self.player.status == PlayerHandStatus.InPlay:
            self.player.hand.add(self.shoe.deal())
            if self.player.hand.bust():
                success = False
        elif self.player.status == PlayerHandStatus.SplitInPlayHandOne:
            self.player.hand.add(self.shoe.deal())
            if self.player.hand.bust():
                self.player.status = PlayerHandStatus.SplitInPlayHandTwo
                success = False
        elif self.player.status == PlayerHandStatus.SplitInPlayHandTwo:
            self.player.split_hand.add(self.shoe.deal())
            if self.player.split_hand.bust():
                self.player.status = PlayerHandStatus.SplitEnded
                success = False
        else:
            self.dealer.hand.add(self.shoe.deal())
            if self.dealer.hand.bust():
                success = False

        return success

    def winner_outcome_and_messaging(self, player_total: int, dealer_total, split_hand:bool = False) -> str:
        """Apply messaging to gaem for game outcome"""
        split_hand_text = ''
        outcome = GameWinner.NotSet

        if self.player.status in (PlayerHandStatus.SplitInPlayHandOne, PlayerHandStatus.SplitInPlayHandTwo,
                                  PlayerHandStatus.SplitEnded):
            if not split_hand:
                split_hand_text = " Hand 1"
            else:
                split_hand_text = " Hand 2"

        if dealer_total < player_total <= 21:
            self.in_game_message += Fore.GREEN + Style.BRIGHT + 'Player wins{}!\n'.format(
                split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.Player
        elif player_total < dealer_total <= 21:
            self.in_game_message += Fore.BLUE + Style.BRIGHT + 'Dealer wins{}!\n'.format(split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.Dealer
        elif player_total > 21:
            self.in_game_message += Fore.BLUE + Style.BRIGHT + 'Dealer wins{}!\n'.format(split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.Dealer
        elif dealer_total > 21:
            self.in_game_message += Fore.GREEN + Style.BRIGHT + 'Player wins{}!\n'.format(
                split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.Player
        else:
            self.in_game_message += Fore.BLACK + Style.BRIGHT + 'No winner{}\n'.format(split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.Draw

        return outcome

    def check_winner(self) -> None:
        """Check if player or dealer is the winner"""

        dealer_total = self.dealer.hand.total()
        player_total = self.player.hand.total()

        self.in_game_message = ''
        self.player.hand.outcome = self.winner_outcome_and_messaging(player_total, dealer_total)

        if self.player.status in (PlayerHandStatus.SplitInPlayHandOne, PlayerHandStatus.SplitInPlayHandTwo,
                                  PlayerHandStatus.SplitEnded):
            self.player.split_hand.outcome = self.winner_outcome_and_messaging(self.player.split_hand.total(), dealer_total, True)

        if self.player.hand.outcome in(GameWinner.Player, GameWinner.Draw) or \
           self.player.split_hand.outcome in(GameWinner.Player, GameWinner.Draw):
            self.calculate_winnings()

    def calculate_winnings(self):
        """Calculate winnings for Player"""

        if not self.player.hand.outcome == GameWinner.Draw:
            # Blackjack pays 3 to 2
            if self.player.hand.blackjack():
                self.player.wallet += (self.bet * (3 / 2))
            else:
                self.player.wallet += self.bet * 2
        else:
            self.player.wallet += self.bet

        if not self.player.split_hand.outcome == GameWinner.NotSet:
            if not self.player.split_hand.outcome == GameWinner.Draw:
                # Blackjack pays 3 to 2
                if self.player.split_hand.blackjack():
                    self.player.wallet += (self.split_bet * (3 / 2))
                else:
                    self.player.wallet += self.split_bet * 2
            else:
                self.player.wallet += self.split_bet


if __name__ == "__main__":
    game = Blackjack(5, 150)
    game.play()
