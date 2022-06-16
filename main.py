# Testing deck
from library.card.entities import Shoe
from library.card.enums import CardValue

if __name__ == '__main__':

    """Find a Royal Flush"""

    shoe = Shoe(100000)
    hand_count = 0

    while shoe.remaining() >= 5:
        card = shoe.deal()
        suit = card.suit
        hand = [card, shoe.deal(), shoe.deal(), shoe.deal(), shoe.deal()]
        hand_count += 1

        hand_filter = filter(lambda target: target.suit == card.suit, hand)
        hand_filter_list = list(hand_filter)

        if len(hand_filter_list) == 5:
            found_ten = False
            found_jack = False
            found_queen = False
            found_king = False
            found_ace = False

            for item in hand_filter_list:
                if item.value == CardValue.Ten:
                    found_ten = True
                elif item.value == CardValue.Jack:
                    found_jack = True
                elif item.value == CardValue.Queen:
                    found_queen = True
                elif item.value == CardValue.King:
                    found_king = True
                elif item.value == CardValue.Ace:
                    found_ace = True

            if found_ten and found_jack and found_queen and found_king and found_ace:
                print('Royal Flush on hand {}'.format(hand_count))
                print(' '.join(str(item) for item in hand))

