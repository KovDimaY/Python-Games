# To run this program you should use the link provided below:
# http://www.codeskulptor.org
# just put all this document to the left part of the screen 
# and press the "play"-button from the menu area


        # Implementation of card game - Memory
# Participants need to find a match for a numbers.
# Player turns over two cards at a time, 
# with the goal of turning over a matching pair

import simplegui # special framework provided by Coursera
import random

deck_of_cards = range(8) + range(8)
index_of_card = 0
state = 0
turns = 0
correct = 0
win = False

expose = range(16)

# helper function to initialize globals
def new_game():
    global deck_of_cards, expose, state, turns, win, correct
    
    temporary = range(16)
    for k in temporary:
         temporary[k] = False
    expose = temporary
    
    state = 0
    turns = 0
    win = False
    correct = 0
    random.shuffle(deck_of_cards)
    label.set_text("Turns = " + str(turns))

     
# define event handlers
def mouseclick(pos):
    global expose, state, previous1_card_index, previous2_card_index
    global same_cards, turns, correct, win
    
    # calculates an index depending on the position of the click
    if ((pos[1] > 0) and (pos[1] < 100)):
        card_index = pos[0] // 50 
        
    # game state logic here
    if (not expose[card_index]):
        if state == 0:
            state = 1
            expose[card_index] = True
            previous1_card_index = card_index
        elif state == 1:
            state = 2
            turns += 1
            label.set_text("Turns = " + str(turns))
            expose[card_index] = True
            
            previous2_card_index = previous1_card_index
            previous1_card_index = card_index
            same_cards = (deck_of_cards[previous1_card_index] == deck_of_cards[previous2_card_index])
            
            if same_cards:
                correct += 1
                if correct == 8:
                    win = True
        else:
            state = 1
            expose[card_index] = True
            if (not same_cards):
                expose[previous1_card_index] = False
                expose[previous2_card_index] = False
            previous1_card_index = card_index
          
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    pos = 5
    ind = 0
    if (win):
        canvas.draw_text("Congratulations!!! You win! :)", (100, 70), 50, 'White')
    else:
        for card in deck_of_cards:
            if expose[ind]:
                canvas.draw_text(str(card), (pos, 75), 70, 'Yellow')
            else:
                canvas.draw_polygon([[pos-5, 0], [pos + 45 , 0], [pos + 45, 100], 
                                     [pos-5, 100]], 3, 'White', 'Green')
            ind += 1
            pos += 50
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
label = frame.add_label("Turns = 0")
label1 = frame.add_label("")
frame.add_button("New Game", new_game, 200)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
