"""Blackjack card game
   https://www.bestuscasinos.org/blog/understanding-5-different-forms-of-blackjack/"""
from colorama import Fore, Style

from src.card.entities import Shoe, Diamonds, Clubs, Spades, Hearts, CardValue
from src.game.entities import BlackJackPlayer, Player
from src.game.enums import GameWinner, PlayerHandStatus
from src.exceptions.game import OutOfFundsException


class Blackjack:
    """Blackjack game class"""
    def __init__(self, shoe_size: int = 1, wallet_amount:float = 100):
        self.game_color = Fore.GREEN + Style.BRIGHT
        self.game_name = self.game_color + '-'*16 + 'Blackjack' + '-'*16 + '\n' \
                  + Style.RESET_ALL
        self.shoe_size = shoe_size
        self.shoe = Shoe(shoe_size)
        self.player = BlackJackPlayer()
        self.player.wallet = wallet_amount
        self.bet:float = 0
        self.split_bet:float = 0
        self.dealer = Player()
        self.game_rules = self.get_rules()
        self.in_game_message = ''
        self.game_blackjack_odds_message = 'blackjack pays (3/2)'

    @staticmethod
    def get_rules() -> str:
        """Get the rules text for the game"""
        rules = ''
        try:
            with open('./library/game/rules/blackjack.txt', 'r') as f:
                rules = f.read()
        except IOError:
            pass

        return rules

    def __str__(self):
        output = '\n' * 50
        output += Fore.LIGHTBLACK_EX + self.game_rules + Style.RESET_ALL + '\n\n'
        output += Fore.BLACK + Style.RESET_ALL + "wallet:\t$" + \
                  str(round(self.player.wallet, 2)) + "\n"
        output += Fore.LIGHTRED_EX + Style.NORMAL + "bet:\t$" + str(round(self.bet, 2)) + "\n"
        if self.split_bet > 0:
            output += Fore.LIGHTRED_EX + Style.NORMAL + "split bet: $" + \
                      str(round(self.split_bet, 2)) + "\n"
        output += self.game_name
        if self.player.status in(PlayerHandStatus.ENDED, PlayerHandStatus.SPLIT_ENDED):
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Dealer ' + Style.RESET_ALL
        output += ' '.join(str(card) for card in self.dealer.hand.cards)
        output += "\n"
        if not self.player.status in(PlayerHandStatus.ENDED, PlayerHandStatus.SPLIT_ENDED):
            output += Fore.BLACK + Style.BRIGHT + '* '
        else:
            output += '  '
        output += Fore.LIGHTBLACK_EX + 'Player ' + Style.RESET_ALL

        if self.player.status in (PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE,
                                  PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO,
                                  PlayerHandStatus.SPLIT_ENDED):
            if self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE:
                output += Fore.BLACK + Style.BRIGHT + "." + Style.RESET_ALL
            output += ' '.join(str(card) for card in self.player.hand.cards)
            output += '|'
            if self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO:
                output += Fore.BLACK + Style.BRIGHT + "." + Style.RESET_ALL
            output += ' '.join(str(card) for card in self.player.split_hand.cards)
        else:
            output += ' '.join(str(card) for card in self.player.hand.cards)

        output += self.game_color + '\n' + '-'*41 + '\n' + Style.RESET_ALL
        output += Fore.LIGHTBLUE_EX + Style.NORMAL + self.game_blackjack_odds_message + '\n' + Style.RESET_ALL
        output += 'remaining cards: {}'.format(self.shoe.remaining())
        output += '\n'
        output += self.in_game_message

        return output

    def reset(self) -> None:
        """Reset game and hands"""
        self.dealer.hand.reset()
        self.player.hand.reset()
        self.player.split_hand.reset()
        self.player.status = PlayerHandStatus.IN_PLAY
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
        valid_bet = 0

        while not valid_entry:
            if self.player.wallet <= 0:
                raise OutOfFundsException

            bet = input('Place your bet: ')

            try:
                valid_bet = int(bet)
                valid_entry = True
            except ValueError:
                try:
                    valid_bet = float(bet)
                    valid_entry = True
                except ValueError:
                    pass

        if self.player.wallet - valid_bet < 0 or valid_bet < 0:
            self.place_your_bets()
        else:
            self.player.wallet -= valid_bet
            self.bet = valid_bet

    def double_down(self):
        """Double down initial bet"""
        if self.player.status == PlayerHandStatus.IN_PLAY and len(self.player.hand.cards) == 1:
            if self.player.wallet - self.bet >= 0:
                self.player.wallet -= self.bet
                self.bet *= 2
        elif self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE and len(self.player.hand.cards) == 1:
            if self.player.wallet - self.bet >= 0:
                self.player.wallet -= self.bet
                self.bet *= 2
        elif self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO and len(self.player.split_hand.cards) == 1:
            if self.player.wallet - self.split_bet >= 0:
                self.player.wallet -= self.split_bet
                self.split_bet *= 2

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
                          '{}R {}to reset deck {}X {}to split {}D {}to double down\n{}Q {}to end '
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
                                  Fore.LIGHTBLACK_EX,
                                  Fore.LIGHTBLUE_EX,
                                  Fore.LIGHTBLACK_EX
                                  ))

            self.in_game_message = ''

            if entry.upper() == 'H':  # Hit
                if not self.hit() and self.player.status is not \
                        PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO:
                    self.check_winner()
                    break
            elif entry.upper() == 'D': # Double down
                self.double_down()
                continue
            elif entry.upper() == 'S':  # Stand
                if self.player.status in(PlayerHandStatus.ENDED, PlayerHandStatus.SPLIT_ENDED):
                    self.check_winner()
                    break
                elif self.player.status == PlayerHandStatus.IN_PLAY:
                    self.player.status = PlayerHandStatus.ENDED
                elif self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE:
                    self.player.status = PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO
                elif self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO:
                    self.player.status = PlayerHandStatus.SPLIT_ENDED
            elif entry.upper() == 'F':  # Fold
                self.in_game_message = Fore.BLUE + Style.BRIGHT + 'Dealer wins!' + Style.RESET_ALL
                break
            elif entry.upper() == 'R':  # Reset deck
                self.shoe.reset()
            elif entry.upper() == 'X':  # Split
                if len(self.player.hand.cards) == 2:
                    if self.player.hand.cards[0].value == self.player.hand.cards[1].value:
                        # Split bet if funds allow
                        if self.player.wallet - self.bet >= 0:
                            self.player.status = PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE
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

        if self.player.status == PlayerHandStatus.IN_PLAY:
            self.player.hand.add(self.shoe.deal())
            if self.player.hand.bust():
                success = False
        elif self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE:
            self.player.hand.add(self.shoe.deal())
            if self.player.hand.bust():
                self.player.status = PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO
        elif self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO:
            self.player.split_hand.add(self.shoe.deal())
            if self.player.split_hand.bust():
                self.player.status = PlayerHandStatus.SPLIT_ENDED
        else:
            self.dealer.hand.add(self.shoe.deal())
            if self.dealer.hand.bust():
                success = False

        return success

    def winner_outcome_and_messaging(self, player_total:
                                     int, dealer_total, split_hand:bool = False) -> str:
        """Apply messaging to gaem for game outcome"""
        split_hand_text = ''
        outcome = GameWinner.NOTSET

        if self.player.status in (PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE,
                                  PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO,
                                  PlayerHandStatus.SPLIT_ENDED):
            if not split_hand:
                split_hand_text = " Hand 1"
            else:
                split_hand_text = " Hand 2"

        if dealer_total < player_total <= 21:
            self.in_game_message += Fore.GREEN + Style.BRIGHT + 'Player wins{}!\n'.format(
                split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.PLAYER
        elif player_total < dealer_total <= 21:
            self.in_game_message += Fore.BLUE + Style.BRIGHT + \
                                    'Dealer wins{}!\n'.format(split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.DEALER
        elif player_total > 21:
            self.in_game_message += Fore.BLUE + Style.BRIGHT + \
                                    'Dealer wins{}!\n'.format(split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.DEALER
        elif dealer_total > 21:
            self.in_game_message += Fore.GREEN + Style.BRIGHT + 'Player wins{}!\n'.format(
                split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.PLAYER
        else:
            self.in_game_message += Fore.BLACK + Style.BRIGHT + \
                                    'No winner{}\n'.format(split_hand_text) + Style.RESET_ALL
            outcome = GameWinner.DRAW

        return outcome

    def check_winner(self) -> None:
        """Check if player or dealer is the winner"""

        dealer_total = self.dealer.hand.total()
        player_total = self.player.hand.total()

        self.in_game_message = ''
        self.player.hand.outcome = self.winner_outcome_and_messaging(player_total, dealer_total)

        if self.player.status in (PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE,
                                  PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO,
                                  PlayerHandStatus.SPLIT_ENDED):
            self.player.split_hand.outcome = self.winner_outcome_and_messaging(
                self.player.split_hand.total(),dealer_total, True)

        if self.player.hand.outcome in(GameWinner.PLAYER, GameWinner.DRAW) or \
           self.player.split_hand.outcome in(GameWinner.PLAYER, GameWinner.DRAW):
            self.calculate_winnings()

    def calculate_winnings(self):
        """Calculate winnings for Player"""

        if self.player.hand.outcome != GameWinner.DRAW:
            # Blackjack pays 3 to 2
            if self.player.hand.blackjack():
                self.player.wallet += (self.bet * (3 / 2))
            else:
                self.player.wallet += self.bet * 2
        else:
            self.player.wallet += self.bet

        if self.player.split_hand.outcome != GameWinner.NOTSET:
            if self.player.split_hand.outcome != GameWinner.DRAW:
                # Blackjack pays 3 to 2
                if self.player.split_hand.blackjack():
                    self.player.wallet += (self.split_bet * (3 / 2))
                else:
                    self.player.wallet += self.split_bet * 2
            else:
                self.player.wallet += self.split_bet


class FaceUp21(Blackjack):
    """Face Up 21, a variation of Blackjack. See readme for rules"""
    def __init__(self, shoe_size: int = 1, wallet_amount: float = 100):
        super().__init__(shoe_size, wallet_amount)
        self.game_color = Fore.BLUE + Style.BRIGHT
        self.game_name = self.game_color + '-' * 16 + 'Face Up 21' + '-' * 15 + '\n' \
                         + Style.RESET_ALL
        self.game_blackjack_odds_message = 'blackjack pays even money'

    @staticmethod
    def get_rules() -> str:
        """Get the rules text for the game"""
        rules = ''
        try:
            with open('./library/game/rules/face_up_21.txt', 'r') as f:
                rules = f.read()
        except IOError:
            pass

        return rules

    def double_down(self):
        """Double down initial bet"""
        if self.player.status == PlayerHandStatus.IN_PLAY and len(self.player.hand.cards) == 1:
            if self.player.hand.cards[0].numerical_value() in (1, 9, 10):
                if self.player.wallet - self.bet >= 0:
                    self.player.wallet -= self.bet
                    self.bet *= 2
        elif self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_ONE and len(self.player.hand.cards) == 1:
            if self.player.hand.cards[0].numerical_value() in (1, 9, 10):
                if self.player.wallet - self.bet >= 0:
                    self.player.wallet -= self.bet
                    self.bet *= 2
        elif self.player.status == PlayerHandStatus.SPLIT_IN_PLAY_HAND_TWO and len(self.player.split_hand.cards) == 1:
            if self.player.split_hand.cards[0].numerical_value() in (1, 9, 10):
                if self.player.wallet - self.split_bet >= 0:
                    self.player.wallet -= self.split_bet
                    self.split_bet *= 2

    def calculate_winnings(self):
        """Calculate winnings for Player"""

        if self.player.hand.outcome != GameWinner.DRAW:
            self.player.wallet += self.bet * 2
        elif self.dealer.hand.blackjack():
            # dealer blackjack beats a player blackjack
            pass
        else:
            self.player.wallet += self.bet

        if self.player.split_hand.outcome != GameWinner.NOTSET:
            if self.player.split_hand.outcome != GameWinner.DRAW:
                self.player.wallet += self.split_bet * 2
            elif self.dealer.hand.blackjack():
                # dealer blackjack beats a player blackjack
                pass
            else:
                self.player.wallet += self.bet

    def place_your_bets(self):
        """Get bet input from user"""
        valid_entry = False
        valid_bet = 0

        while not valid_entry:
            if self.player.wallet <= 0:
                raise OutOfFundsException

            bet = input('Place your bet: ')

            try:
                valid_bet = int(bet)
                valid_entry = True
            except ValueError:
                try:
                    valid_bet = float(bet)
                    valid_entry = True
                except ValueError:
                    pass

        if self.player.wallet - valid_bet < 0 or valid_bet < 0:
            self.place_your_bets()
        else:
            self.player.wallet -= valid_bet
            self.bet = valid_bet

            self.dealer.hand.add(self.shoe.deal())
            self.dealer.hand.add(self.shoe.deal())
            self.player.hand.add(self.shoe.deal())

    def play(self) -> None:
        """Game logic to run the game"""
        keep_playing = ''

        try:
            while keep_playing != 'Q':
                keep_playing = self.process_input()
                print(self)
                self.reset()

        except IndexError:
            print(Fore.RED + Style.BRIGHT + 'Out of cards' + Style.RESET_ALL)
        except OutOfFundsException:
            print(Fore.RED + Style.BRIGHT + 'Out of funds' + Style.RESET_ALL)


class Spanish21(Blackjack):
    """Spanish 21, a variation of Blackjack. See readme for rules"""
    def __init__(self, shoe_size: int = 1, wallet_amount: float = 100):
        super().__init__(shoe_size, wallet_amount)
        self.game_color = Fore.RED + Style.BRIGHT
        self.game_name = self.game_color + '-' * 16 + 'Spanish 21' + '-' * 15 + '\n' \
                         + Style.RESET_ALL
        self.game_blackjack_odds_message = 'blackjack pays (3/2)'
        self.remove_tens()
        self.shoe.notifier.subscribe("reset", self.remove_tens)

    @staticmethod
    def get_rules() -> str:
        """Get the rules text for the game"""
        rules = ''
        try:
            with open('./library/game/rules/spanish_21.txt', 'r') as f:
                rules = f.read()
        except IOError:
            pass

        return rules

    def remove_tens(self):
        """Spanish 21 does not have 10s"""
        self.shoe.remove(Diamonds(CardValue.TEN))
        self.shoe.remove(Hearts(CardValue.TEN))
        self.shoe.remove(Clubs(CardValue.TEN))
        self.shoe.remove(Spades(CardValue.TEN))

    def apply_odds(self, hand):
        """Apply odds"""

        values = hand.values()

        # Blackjack always wins, and is always paid 3:2 regardless of whether or not the dealer has a blackjack.
        if hand.blackjack():
            self.player.wallet += (self.bet * (3 / 2))
        elif hand.total() == 21 and len(hand.cards) == 5:
            # A five-card 21 pays out at 3:2
            self.player.wallet += (self.bet * (3 / 2))
        elif hand.total() == 21 and len(hand.cards) == 6:
            # A Six-card 21 pays 2:1
            self.player.wallet += (self.bet * (2 / 1))
        elif hand.total() == 21 and len(hand.cards) == 7:
            # A seven-card 21 pays out at 3:1.
            self.player.wallet += (self.bet * (3 / 1))
        elif len(hand.cards) == 3 and hand.all_same_suit() and values.count(7) == 3:
            # 777 of same suit pays 2:1
            self.player.wallet += (self.bet * (2 / 1))
            # If a player has 777 of the same suit and the dealer is holding a 7 in any suit, there
            # is a $1,000 bonus paid to the player.
            # If the player has bet more than $25 at the start of the hand, this climbs all the way to $5,000.
            if self.dealer.hand.has_card(CardValue.SEVEN):
                if self.bet > 25:
                    self.player.wallet += 5000
                else:
                    self.player.wallet += 1000
        elif len(hand.cards) == 3 and values.count(7) == 3:
            # A 777 of mixed suit pays 3:2.
            self.player.wallet += (self.bet * (3 / 2))
        elif len(hand.cards) == 3 and hand.all_same_suit() and values.count(6) == 1 and values.count(7) == 1 and values.count(8) == 1:
            # A 678 of same suit pays 2:1.
            self.player.wallet += (self.bet * (2 / 1))
        elif len(hand.cards) == 3 and values.count(6) == 1 and values.count(7) == 1 and values.count(8) == 1:
            # A 678 of mixed suit pays 3:2.
            self.player.wallet += (self.bet * (3 / 2))
        else:
            self.player.wallet += self.bet * 2

    def calculate_winnings(self):
        """Calculate winnings for Player"""

        if self.player.hand.outcome != GameWinner.DRAW or self.player.hand.blackjack():
            self.apply_odds(self.player.hand)
        else:
            self.player.wallet += self.bet

        if self.player.split_hand.outcome != GameWinner.NOTSET:
            if self.player.split_hand.outcome != GameWinner.DRAW or self.player.split_hand.blackjack():
                # Blackjack pays 3 to 2
                self.apply_odds(self.player.split_hand)
            else:
                self.player.wallet += self.split_bet


class BlackjackGameCollection:
    def __init__(self, shoe_size: int = 1, wallet_amount: float = 100):
        self.games = (Blackjack, FaceUp21, Spanish21)
        self.size = shoe_size
        self.wallet_amount = wallet_amount

    def select_game(self):
        game_selection = -1

        while not(0 <= game_selection <=2):
            player_input = input('Select a game to play\n\n1\tBlackjack\n2\tFace Up 21\n3\tSpanish 21\n')
            try:
                game_selection = int(player_input) - 1
            except ValueError:
                continue

        self.play(game_selection)

    def play(self, game_selection:int = 0):
        self.games[game_selection](self.size, self.wallet_amount).play()



