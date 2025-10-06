import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# Constants
CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_FOLDER = 'cards'  # Ensure this folder exists with all card images

# Define Card Class
class Card:
    def __init__(self, rank, suit):
        self.rank = rank.lower()
        self.suit = suit.lower()

    def value(self):
        if self.rank in ['jack', 'queen', 'king']:
            return 10
        elif self.rank == 'ace':
            return 11  # Initially, ace is counted as 11
        else:
            return int(self.rank)

    def image_filename(self):
        return f"{self.rank}_of_{self.suit}.png"

# Define Deck Class
class Deck:
    def __init__(self):
        self.cards = []
        self.initialize_deck()
        self.shuffle()

    def initialize_deck(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                 'jack', 'queen', 'king', 'ace']
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) == 0:
            self.initialize_deck()
            self.shuffle()
        return self.cards.pop()

# Define Hand Class
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self, hide_first_card=False):
        value = 0
        aces = 0
        for idx, card in enumerate(self.cards):
            if hide_first_card and idx == 0:
                continue  # Skip hidden dealer card
            value += card.value()
            if card.rank == 'ace':
                aces += 1
        # Adjust for aces if value > 21
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def is_bust(self):
        return self.calculate_value() > 21

    def has_blackjack(self):
        return self.calculate_value() == 21 and len(self.cards) == 2

# Define Blackjack Game Class
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def initial_deal(self):
        # Player gets two cards
        self.player_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        # Dealer gets two cards
        self.dealer_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

    def player_hit(self):
        self.player_hand.add_card(self.deck.deal_card())

    def dealer_hit(self):
        self.dealer_hand.add_card(self.deck.deal_card())

    def reset_game(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

# Define Blackjack GUI Class
class BlackjackGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.geometry("1000x700")
        self.resizable(True, True)

        # Initialize Game
        self.game = BlackjackGame()
        self.game.initial_deal()

        # Load Images
        self.card_images = {}
        self.load_card_images()

        # Create GUI Components
        self.create_widgets()

        # Display Initial Hands
        self.display_initial_hands()

    def load_card_images(self):
        # Load all card images
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                 'jack', 'queen', 'king', 'ace']
        for suit in suits:
            for rank in ranks:
                filename = f"{rank}_of_{suit}.png"
                path = os.path.join(CARD_FOLDER, filename)
                if os.path.exists(path):
                    image = Image.open(path).resize((CARD_WIDTH, CARD_HEIGHT))
                    self.card_images[f"{rank}_of_{suit}"] = ImageTk.PhotoImage(image)
                else:
                    print(f"Missing image: {path}")
                    # Optionally, use a placeholder or skip
        # Load back of card image
        back_path = os.path.join(CARD_FOLDER, "back_of_card.png")
        if os.path.exists(back_path):
            image = Image.open(back_path).resize((CARD_WIDTH, CARD_HEIGHT))
            self.card_images["back"] = ImageTk.PhotoImage(image)
        else:
            print(f"Missing image: {back_path}")
            # Create a solid color image as placeholder
            placeholder = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), color='green')
            self.card_images["back"] = ImageTk.PhotoImage(placeholder)

    def create_widgets(self):
        # Frames for Dealer and Player
        self.dealer_frame = tk.Frame(self)
        self.dealer_frame.pack(pady=20)

        self.dealer_value_label = tk.Label(self, text="Dealer's Hand Value: ", font=("Helvetica", 14))
        self.dealer_value_label.pack()

        self.player_frame = tk.Frame(self)
        self.player_frame.pack(pady=20)

        self.player_value_label = tk.Label(self, text="Player's Hand Value: ", font=("Helvetica", 14))
        self.player_value_label.pack()

        # Frame for Buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=20)

        # Buttons
        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit, width=12, height=2)
        self.hit_button.pack(side=tk.LEFT, padx=20)

        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand, width=12, height=2)
        self.stand_button.pack(side=tk.LEFT, padx=20)

        self.message_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.message_label.pack(pady=10)

        self.play_again_button = tk.Button(self.button_frame, text="Play Again", command=self.play_again, width=12, height=2, state=tk.DISABLED)
        self.play_again_button.pack(side=tk.LEFT, padx=20)

    def display_initial_hands(self):
        # Display Player's Cards
        for card in self.game.player_hand.cards:
            self.display_card(self.player_frame, card)

        # Display Dealer's First Card
        self.display_card(self.dealer_frame, self.game.dealer_hand.cards[0])

        # Display Back of Card for Dealer's Second Card
        self.dealer_hidden_card_label = tk.Label(self.dealer_frame, image=self.card_images["back"])
        self.dealer_hidden_card_label.pack(side=tk.LEFT, padx=10)

        # Update Hand Values
        player_value = self.game.player_hand.calculate_value()
        self.player_value_label.config(text=f"Player's Hand Value: {player_value}")

        # Dealer's visible card value
        dealer_visible_card = self.game.dealer_hand.cards[0]
        dealer_value = dealer_visible_card.value()
        if dealer_visible_card.rank == 'ace':
            dealer_value = 11
        self.dealer_value_label.config(text=f"Dealer's Hand Value: {dealer_value}")

    def display_card(self, frame, card):
        image_key = f"{card.rank}_of_{card.suit}"
        if image_key in self.card_images:
            card_image = self.card_images[image_key]
        else:
            # Use back image or placeholder if missing
            card_image = self.card_images["back"]
        card_label = tk.Label(frame, image=card_image)
        card_label.image = card_image  # Prevent garbage collection
        card_label.pack(side=tk.LEFT, padx=10)

    def hit(self):
        if self.game.player_hand.calculate_value() >= 21:
            return  # No action if player already has 21 or busts

        self.game.player_hit()
        new_card = self.game.player_hand.cards[-1]
        self.display_card(self.player_frame, new_card)

        player_score = self.game.player_hand.calculate_value()
        self.player_value_label.config(text=f"Player's Hand Value: {player_score}")

        if player_score > 21:
            self.message_label.config(text="Player Busts! Dealer Wins.")
            self.end_game()

    def stand(self):
        # Disable Hit and Stand buttons
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

        # Reveal Dealer's Hidden Card
        dealer_hidden_card = self.game.dealer_hand.cards[1]
        self.dealer_hidden_card_label.config(image=self.card_images[f"{dealer_hidden_card.rank}_of_{dealer_hidden_card.suit}"])
        self.dealer_hidden_card_label.image = self.card_images[f"{dealer_hidden_card.rank}_of_{dealer_hidden_card.suit}"]  # Prevent GC

        # Update Dealer's Hand Value
        dealer_value = self.game.dealer_hand.calculate_value()
        self.dealer_value_label.config(text=f"Dealer's Hand Value: {dealer_value}")

        # Dealer's Turn
        while True:
            dealer_score = self.game.dealer_hand.calculate_value()
            if dealer_score < 17:
                self.game.dealer_hit()
                new_card = self.game.dealer_hand.cards[-1]
                self.display_card(self.dealer_frame, new_card)
                dealer_score = self.game.dealer_hand.calculate_value()
                self.dealer_value_label.config(text=f"Dealer's Hand Value: {dealer_score}")
            elif dealer_score == 17 and self.is_soft_17():
                self.game.dealer_hit()
                new_card = self.game.dealer_hand.cards[-1]
                self.display_card(self.dealer_frame, new_card)
                dealer_score = self.game.dealer_hand.calculate_value()
                self.dealer_value_label.config(text=f"Dealer's Hand Value: {dealer_score}")
            else:
                break

        # Determine Outcome
        self.determine_winner()

    def is_soft_17(self):
        value = 0
        aces = 0
        for card in self.game.dealer_hand.cards:
            value += card.value()
            if card.rank == 'ace':
                aces += 1
        # Adjust for aces
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value == 17 and aces > 0

    def determine_winner(self):
        player_value = self.game.player_hand.calculate_value()
        dealer_value = self.game.dealer_hand.calculate_value()

        if self.game.dealer_hand.is_bust():
            self.message_label.config(text="Dealer Busts! Player Wins.")
        elif dealer_value > player_value:
            self.message_label.config(text="Dealer Wins.")
        elif dealer_value < player_value:
            self.message_label.config(text="Player Wins!")
        else:
            self.message_label.config(text="It's a Tie!")

        self.end_game()

    def end_game(self):
        # Disable Hit and Stand buttons
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        # Enable Play Again button
        self.play_again_button.config(state=tk.NORMAL)

    def play_again(self):
        # Reset the game state
        self.game.reset_game()
        self.message_label.config(text="")

        # Clear all card displays
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

        # Display new hands
        self.game.initial_deal()
        self.display_initial_hands()

        # Re-enable Hit and Stand buttons
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        # Disable Play Again button
        self.play_again_button.config(state=tk.DISABLED)

# Run the game
if __name__ == "__main__":
    # Check if card images exist
    required_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                      'jack', 'queen', 'king', 'ace']
    required_suits = ['hearts', 'diamonds', 'clubs', 'spades']
    missing_images = []
    for suit in required_suits:
        for rank in required_ranks:
            filename = f"{rank}_of_{suit}.png"
            path = os.path.join(CARD_FOLDER, filename)
            if not os.path.exists(path):
                missing_images.append(path)
    # Check for back of card
    back_path = os.path.join(CARD_FOLDER, "back_of_card.png")
    if not os.path.exists(back_path):
        missing_images.append(back_path)

    if missing_images:
        error_message = "Missing card images:\n" + "\n".join(missing_images)
        print(error_message)
        # Initialize a temporary root to show messagebox
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the main window
        messagebox.showerror("Missing Images", error_message)
    else:
        app = BlackjackGUI()
        app.mainloop()

