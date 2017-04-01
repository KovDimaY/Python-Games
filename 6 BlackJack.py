# To run this program you should use the link provided below:
# http://www.codeskulptor.org
# just put all this document to the left part of the screen 
# and press the "play"-button from the menu area

				# Blackjack

import simplegui # special framework provided by Coursera
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
dealer_score = 0
player_score = 0
computer_win = False

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, 
						  [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        result = "Hand contains"
        for card in self.cards:
            result += " " + str(card)
        return result

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, 
		# then add 10 to hand value if it doesn't bust
        result = 0
        is_ace = False
        for card in self.cards:
            result += VALUES[card.get_rank()]
            if (card.get_rank() == "A"):
                is_ace = True
        if ((is_ace) and (result + 10 <= 21)):
            result += 10
        return result
    
    def draw(self, canvas, y_pos):
        x_pos = 50
        for card in self.cards:
            card.draw(canvas, (x_pos, y_pos))
            x_pos += 80 
    
    
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        result = ""
        for card in self.cards:
            result += " " + str(card)
        return result

#define global variables for game
game_deck = Deck()
player_hand = Hand()
dealer_hand = Hand()

#helper methods

def score_format(x, y):
    result = ""
    if (x < 10):
        result = result + "0" + str(x)
    else:
        result += str(x)
    result += " : "
    if (y < 10):
        result = result + "0" + str(y)
    else:
        result += str(y)
    return result
   
   
#define event handlers for buttons
def deal():
    global outcome, in_play, game_deck, player_hand, dealer_hand, computer_win, dealer_score
    game_deck = Deck()
    game_deck.shuffle()
	
    player_hand = Hand()
    dealer_hand = Hand()
	
    player_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())
    player_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())
	
    if in_play:
        dealer_score += 1  
    in_play = True
    computer_win = False

        
def hit():
    global player_hand, dealer_score, in_play
 
    if in_play:
        player_hand.add_card(game_deck.deal_card())
        if (player_hand.get_value() > 21):
            in_play = False
            dealer_score += 1
        
   
# if busted, assign a message to outcome, update in_play and score
def stand():
    global in_play, dealer_score, player_score, computer_win
    if in_play:
        if dealer_hand.get_value() < player_hand.get_value():
            while ((dealer_hand.get_value() <= 18) or 
				   (dealer_hand.get_value() < player_hand.get_value())):
                    dealer_hand.add_card(game_deck.deal_card())
            in_play = False
            
			if ((dealer_hand.get_value() <= 21) and 
				(dealer_hand.get_value() >= player_hand.get_value())):
                dealer_score += 1
                computer_win = True
            else:
                player_score += 1
        else:
            in_play = False
            dealer_score += 1
            computer_win = True
        
   
# draw handler    
def draw(canvas):
    canvas.draw_text('Blackjack', (230, 100), 80, 'Black')
    canvas.draw_text('Dealer hand', (30, 180), 40, 'White')    
    canvas.draw_text('Your hand', (40, 370), 40, 'Yellow')
	dealer_hand.draw(canvas, 200)    
    player_hand.draw(canvas, 390)
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (86,248), CARD_BACK_SIZE)
    
    if (player_hand.get_value() <= 21):
        canvas.draw_text('Hand value: ' + str(player_hand.get_value()), (70, 520), 20, 'Black')
        if ((not in_play) and computer_win):
            canvas.draw_text('You loose! ' , (530, 500), 55, 'Red')
            canvas.draw_text('Press "Deal" button to play one more hand... ' , (140, 570), 30, 'Lime')
        elif (not in_play):
            canvas.draw_text('You win! ' , (550, 500), 55, 'Red')
            canvas.draw_text('Press "Deal" button to play one more hand... ' , (140, 570), 30, 'Lime')
        else:
            canvas.draw_text('Hit or Stand?' , (450, 550), 55, 'Red')
            canvas.draw_text('If You press "Deal" button, dealer wins immediately!' , (440, 570), 15, 'LightPink')
    else:
        canvas.draw_text('You bust! ' , (550, 500), 55, 'Red')
        canvas.draw_text('Press "Deal" button to play one more hand... ' , (140, 570), 30, 'Lime')
        
    canvas.draw_text('Score', (550, 280), 90, 'Orange')
    canvas.draw_text('Dealer / You', (600, 300), 20, 'Black')
    canvas.draw_text(score_format(dealer_score, player_score), (570, 360), 60, 'White')
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# print the rules of the game
label1 = frame.add_label('Rules:')
label1 = frame.add_label('Counting any ace as 1 or 11,')
label1 = frame.add_label('as a player wishes, any face')
label1 = frame.add_label('card as 10, and any other')
label1 = frame.add_label('card at its pip value, each')
label1 = frame.add_label('participant attempts to beat')
label1 = frame.add_label('the dealer by getting a count')
label1 = frame.add_label('as close to 21 as possible,')
label1 = frame.add_label('without going over 21.')
label1 = frame.add_label('')
label1 = frame.add_label('If You have as much points as')
label1 = frame.add_label('dealer does, then dealer wins the hand.')

# get things rolling
deal()
frame.start()