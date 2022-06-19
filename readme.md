# Blackjack Game Collection

### **BlackjackGameCollection**

This is the game collection class that is used to start one of the three games as detailed below.
Create a new instance of this class and call the select_game method to request player input on game selection

game = BlackjackGameCollection()

game.select_game()

#### Parameters

* shoe_size (int): Number of decks in the shoe. Defaults to 1
* wallet_amount (float): Starting wallet for player. Defaults to 100
* display_rules (bool): Display the rules of the game or not. Defaults to True

### Blackjack

_Rules_
1. Blackjack pays 3/2
2. The dealer hits on 16 and stands on 17.

### FaceUp21

Rules
1. In this version of the game, both of the dealer’s cards are dealt and shown face up.
2. Dealer hits on soft 17, and dealer blackjack beats a player blackjack, and blackjack only pays even money.
3. Players can only double down on 9, 10, and 11.

### Spanish21

Rules
1. A five-card 21 pays out at 3:2 
2. A Six-card 21 pays 2:1
3. A seven-card 21 pays out at 3:1.
4. A 678 and 777 of mixed suit pays 3:2. If they’re the same suit it pays 2:1.
5. If a player has 777 of the same suit and the dealer is holding a 7 in any suit, there is a $1,000 bonus paid to the player.
6. If the player has bet more than $25 at the start of the hand, this climbs all the way to $5,000.
7. Blackjack always wins, and is always paid 3:2 regardless of whether or not the dealer has a blackjack.
8. Like traditional blackjack, the dealer hits on 16 and stands on 17

