import random

# Constants
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

# Deck class
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

# Hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # Track aces in hand

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'A':
            self.aces += 1

    def adjust_for_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        return ', '.join([str(card) for card in self.cards])

# Game logic
def play_blackjack():
    # Initialize deck, hands, and chips
    deck = Deck()

    player_hand = Hand()
    dealer_hand = Hand()

    # Deal initial two cards to player and dealer
    for _ in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

    # Adjust hand for aces
    player_hand.adjust_for_aces()
    dealer_hand.adjust_for_aces()

    # Display cards
    print("Dealer's hand: <Hidden>,", dealer_hand.cards[1])
    print(f"Player's hand: {player_hand} (value: {player_hand.value})\n")

    # Player turn
    while True:
        choice = input("Do you want to hit or stand? (h/s): ").lower()
        if choice == 'h':
            player_hand.add_card(deck.deal_card())
            player_hand.adjust_for_aces()
            print(f"Player's hand: {player_hand} (value: {player_hand.value})")

            if player_hand.value > 21:
                print("Player busts! Dealer wins.")
                return
        elif choice == 's':
            break
        else:
            print("Invalid input. Please enter 'h' to hit or 's' to stand.")

    # Dealer turn
    print(f"\nDealer's hand: {dealer_hand} (value: {dealer_hand.value})")

    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.adjust_for_aces()
        print(f"Dealer's hand: {dealer_hand} (value: {dealer_hand.value})")

        if dealer_hand.value > 21:
            print("Dealer busts! Player wins.")
            return

    # Determine the winner
    if dealer_hand.value > player_hand.value:
        print("Dealer wins!")
    elif dealer_hand.value < player_hand.value:
        print("Player wins!")
    else:
        print("It's a tie!")

# Run the game
if __name__ == "__main__":
    while True:
        play_blackjack()
        replay = input("\nDo you want to play again? (y/n): ").lower()
        if replay != 'y':
            break
