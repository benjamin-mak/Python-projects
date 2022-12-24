#Import functions
import random 
from IPython.display import clear_output

# Global variables
suits = ("Clubs", "Diamonds", "Hearts", "Spades")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {"Two":2, "Three":3, "Four":4, "Five":5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':10}

# Card class
class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

# Deck class
class Deck():
    def __init__(self):
        self.deck_cards = []
        for suit in suits:
            for rank in ranks:
                self.deck_cards.append(Card(suit,rank))
    
    # method for shuffling the deck
    def shuffle(self):
        random.shuffle(self.deck_cards)
    
    # method for dealing cards
    def deal_one(self):
        return self.deck_cards.pop()

    # returns number of cards in the deck
    def __len__(self):
        return len(self.deck_cards)

# Player class
class Player():
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.value = 0
        self.ace = 0    #keep track of number of aces in hand

    # add cards to hand
    def add_card(self, new_card):
        self.cards.append(new_card)
        self.value += values[new_card.rank]
        if new_card.rank == "Ace":
            self.ace += 1

    #adjust hand value if there is an ace
    def adjust_ace(self):
        while self.value > 21 and self.ace > 0:
            self.value -= 9
            self.ace -= 1 

    #add 1 point for when Ace is equal to 11
    def ace_11(self):
        if len(self.cards) == 2 and self.ace == 1:
            self.value += 1

    #subtract 1 point if player draws a card
    def ace_10(self):
        if len(self.cards) == 2 and self.ace == 1:
            self.value -= 1

    #reset player's hand, removes all cards for a new round
    def reset_hand(self):
        self.cards = []
        self.value = 0
        self.ace = 0 
        
    def __str__(self):
        return f"{self.name} currently has {self.value} points. "

# Player's chips class
class Chips():
    def __init__(self, amount=0):
        self.amount = amount

    def win_bet(self, win_amt):
        self.amount += win_amt

    def lose_bet(self, lose_amt):
        self.amount -= lose_amt

    def __str__(self):
        return f"You currently have ${self.amount} left."

#Game functions
def player_bet(player_chips):
          
    while True:

        bet_amount = input("Please enter an amount to bet. You can only bet in multiples of $1.")

        if not bet_amount.isdigit():
            print("Please enter only numbers and in multiples of $1!")
            continue
        else:
            bet_amount = int(bet_amount)
        
        if bet_amount > player_chips.amount:
            print(f"You don't have enough chips for that bet. You have ${player_chips.amount} left. Please enter another amount.")
            continue
        else:
            break
  
    return bet_amount

def player_bust(player_hand):
    return player_hand.value > 21

def display_hand(player_hand):
    print(f"{player_hand.name}'s hand has {player_hand.value} points.")
    print(f"Cards in {player_hand.name}'s hand: ", *player_hand.cards,sep=", ") 

def blackjack(hand):

    num_aces = 0
    num_face = 0
    for i in hand.cards:
        if i.rank == "Ace":
            num_aces += 1
        elif i.rank in ['Ten', 'Jack', 'Queen', 'King']:
            num_face += 1
    
    return num_aces == 2 or (num_aces == 1 and num_face == 1)

def hit(deck, hand):
    #subtract 1 point if there is an Ace already in hand
    hand.ace_10()
    #Add 1 card to hand
    hand.add_card(deck.deal_one())
    #adjust hand value if there is an Ace
    hand.adjust_ace()
    print(f"{hand.cards[-1]} was drawn.")

def hit_or_stand(player_hand):
    
    decision = 'wrong'
   
    while decision not in [1,2]:
        decision = input("Do you want to hit or stand? Type 1 to draw a card, type 2 to stand.")
        if not decision.isdigit():
            print("Invalid input! Please type 1 to draw a card or 2 to stand.")
            continue
        else:
            decision = int(decision)

    if decision == 2 and player_hand.value < 15:
        print("You don't have enough points, you need at least 15 to stand. You need to draw a card.")
        decision = 1

    return decision == 1 

def outcome(player_hand, dealer_hand, status):

    if dealer_hand.value > player_hand.value and not player_bust(dealer_hand):
        status = 'lose'
        print(f"You lose! Dealer has {dealer_hand.value} points, you only have {player_hand.value} points.")
    elif dealer_hand.value == player_hand.value:
        status = 'draw'
        print(f"It's a draw, you both have {player_hand.value} points.")
    elif dealer_hand.value > 21:
        status = 'win'
        print("Dealer bust! You win!")
    else:
        status = 'win'
        print("You win! You have more points than the dealer!")
    
    return status

def new_round():
 
    play = 'wrong'

    while play not in ['y', 'n']:
        play = input("Do you want to play another round? Type 'y' to play another round, type 'n' to end the game and cash out.")
        
        if play not in ['y', 'n']:
            print("Please type 'y' or 'n'.")

    return play == 'y'

#Setup the game
#Player and dealer variables
name = input("Please enter your name:")
player = Player(name)
dealer = Player("Dealer")

#Player's starting amount
while True:
    buy_in = input("Please enter your buy-in amount:")
    if not buy_in.isdigit():
        print("Please only enter numbers!")
        continue
    else:
        buy_in = int(buy_in)
        break

player_chips = Chips(buy_in)
print(f"Welcome {name} to the game of blackjack! You bought in with ${player_chips.amount}.")

#While loop to get the game going
game_on = True
while game_on:
    
    #Reset hands
    player.reset_hand()
    dealer.reset_hand()

    #Create a new deck of 52 cards and shuffle the deck
    new_deck = Deck()
    new_deck.shuffle()

    #Create a counter for player status (win/lose/draw/bust)
    status = ''

    #Display total amount, ask player to place bet, check if bet amount is more than the current total chips
    print(player_chips)
    bet_amt = player_bet(player_chips)
    print(f"You have placed a bet of ${bet_amt}.")

    #Create a for loop to add cards to dealer and players hand. Show the first item in the list of the dealer.
    for i in range(2):
        player.add_card(new_deck.deal_one())
        dealer.add_card(new_deck.deal_one())
    print(f"Dealer's first card is: {dealer.cards[0]}")
    #add 1 point if there is an Ace in hand
    player.ace_11()
    dealer.ace_11()
    display_hand(player)

    #Check if anyone has 21 (an ace and a 10 or face card, or 2 aces)
    if blackjack(player) and blackjack(dealer):
        status = 'draw'
        print("It's a draw, both you and the dealer have blackjack.")
        display_hand(player)
        display_hand(dealer)
    elif blackjack(player) and not blackjack(dealer):
        status = 'win'
        print("You have blackjack! You win!")
        display_hand(player)
    elif not blackjack(player) and blackjack(dealer):
        status = 'lose'
        print("You lose! Dealer has blackjack!")
        display_hand(dealer)
    else:
        pass
    
    while status == '':
        #Player's turn
        #While player's total points is <= 21, ask player to hit or stand
        while player.value <= 21:
            #if player chooses hit
            if hit_or_stand(player):
                #add card to player's hand
                hit(new_deck, player)
                #display player's hand
                display_hand(player)
            #else if player chooses stand
            else:
                break

        #Check player status, break out of loop if player busts
        if player_bust(player):
            status = 'lose'
            print("Bust! You have more than 21 points!")
            break

        #Dealer's turn
        print("Dealer's turn!")
        #While dealer's total points is less than player's total points
        while dealer.value < player.value:
            #dealer draws a card, display the card and total points
            hit(new_deck, dealer)
            print(f"Dealer has {dealer.value} points.")
        
        #Compare hands and determine the winner
        status = outcome(player, dealer, status)
        display_hand(dealer)

    #if player status equal win, add chips
    if status == 'win':
        player_chips.win_bet(bet_amt)
        print(f"${bet_amt} has been added.")
    #if player status equal to lose or bust, deduct chips
    elif status == 'lose':
        player_chips.lose_bet(bet_amt)
        print(f"${bet_amt} has been deducted.")
    #if status equals draw, do nothing
    else:
        print("Draw. $0 has been added.")
        pass
    
    print(f"You have ${player_chips.amount} remaining.")

    #Check whether player has enough balance chips to play another round
    if player_chips.amount <= 0:
        break

    #Ask player if he wants to play another round
    if not new_round():
        game_on = False
    
    print("------------------------------------------------------------------------------------")
    clear_output()

#Print total amount left 
print(f"Game has ended. You bought in with ${buy_in}. You have ${player_chips.amount} left.")
