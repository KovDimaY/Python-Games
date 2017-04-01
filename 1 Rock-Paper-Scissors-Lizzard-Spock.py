# To run this program you should use the link provided below:
# http://www.codeskulptor.org
# just put all this document to the left part of the screen 
# and press the "play"-button from the menu area


			# Rock-paper-scissors-lizard-Spock
 
import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    if (name == "rock"):
        return 0
    elif (name == "Spock"):
        return 1
    elif (name == "paper"):
        return 2
    elif (name == "lizard"):
        return 3
    else :
        return 4


def number_to_name(number):
    if (number == 0):
        return "rock"
    elif (number == 1):
        return "Spock"
    elif (number == 2):
        return "paper"
    elif (number == 3):
        return "lizard"
    else :
        return "scissors"
    
# Game code

def rpsls(player_choice): 
    
    # Compute player's number
    player_number = name_to_number(player_choice)
    
    # Select computer's number
    computer_number = random.randrange(0, 5)
    
    # Select computer's choice
    computer_choice = number_to_name(computer_number)
    
    # Computing of winner
    if ( (player_number - computer_number) % 5 == 1 ):
        print "Player chooses ", player_choice
        print "Computer chooses ", computer_choice
        print "Player wins!!!"
        print
        
    elif ( (player_number - computer_number) % 5 == 2 ):
        print "Player chooses ", player_choice
        print "Computer chooses ", computer_choice
        print "Player wins!!!"
        print
     
    elif ( (player_number - computer_number) % 5 == 3 ):
        print "Player chooses ", player_choice
        print "Computer chooses ", computer_choice
        print "Computer wins!!!"
        print
           
    elif ( (player_number - computer_number) % 5 == 4 ):
        print "Player chooses ", player_choice
        print "Computer chooses ", computer_choice
        print "Computer wins!!!"
        print
        
    elif ( (player_number - computer_number) % 5 == 0 ):
        print "Player chooses ", player_choice
        print "Computer chooses ", computer_choice
        print "Player and computer tie!!!"
        print
      
    
# test of code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")


