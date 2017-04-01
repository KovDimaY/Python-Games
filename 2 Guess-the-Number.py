# To run this program you should use the link provided below:
# http://www.codeskulptor.org
# just put all this document to the left part of the screen 
# and press the "play"-button from the menu area


				# "Guess the number" 
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui # special framework provided by Coursera
import random

# global range of games (player can change it in game modes)
range_of_game = 100

secret_number = 0
attempts = 0

# helper function to draw text
def draw_handler(canvas):
    canvas.draw_text('Have', (70, 50), 32, 'Red')
    canvas.draw_text('a', [95, 100], 32, 'Blue')
    canvas.draw_text('GOOD', [55, 150], 32, 'Yellow')
    canvas.draw_text('Day!', (70, 200), 32, 'Green')
    canvas.draw_text(':)', [90, 250], 32, 'Purple')

# helper function to start and restart the game
def new_game():
    global attempts, secret_number
    print "\n\n***************************************"
    print "        New game in range ", range_of_game
    print "***************************************"
    
    # set the number of attempts 
    if (range_of_game == 100):
        attempts = 7
    else:
        attempts = 10
    
    print "You have ", attempts, " attempts to win the game!\n"
    
    # set the secret number
    secret_number = random.randrange(1, range_of_game)

    
# define event handlers for control panel
def range100():
    global range_of_game
    range_of_game = 100
    new_game()    
   
def range1000():
    global range_of_game
    range_of_game = 1000
    new_game()
    

# MAIN PROCEDURE
def input_guess(guess):
    global attempts
    guess = int(guess)
    attempts = attempts - 1
    
    if ((attempts < 1) and (guess != secret_number)):
        print "Your guess is", guess
        print "Sorry, but computer wins!"
        print "Secret number was", secret_number
        new_game()
    else:
        print "Your guess is", guess
    
        if (guess == secret_number):
            print "Congratulations!!! You win!" 
            print "The secret number is", secret_number
            new_game()
        elif (guess > secret_number):
            print "Secret number is less..."
            print "But You still have", attempts, "attepts to win the game!\n"
        else:
            print "Secret number is bigger..."
            print "But You still have", attempts, "attepts to win the game!\n"   
    

# create frame
frame = simplegui.create_frame("Guess the number", 200, 300, 300)
frame.set_draw_handler(draw_handler)

# register event handlers for control elements and start frame
frame.add_button("Start easy game (0-100)", range100, 300)
frame.add_button("Start hard game (0-1000)", range1000, 300)
frame.add_input("Enter your guess:", input_guess, 100)

# START THE GAME 
frame.start()
new_game()
