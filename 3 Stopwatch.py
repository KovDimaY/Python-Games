# To run this program you should use the link provided below:
# http://www.codeskulptor.org
# just put all this document to the left part of the screen 
# and press the "play"-button from the menu area


			#"Stopwatch: The Game"#
# Rules: Player has to press the button "Stop Timer"
# in the moment when the timer will show a time
# with whole number of seconds (milliseconds = 0)

# special framework provided by Coursera
import simplegui

# define global variables
time = 0
succeses = 0
attempts = 0
score = 100
string_result = "0/0"

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format_time(t):
    result = ""
    
    # find out minutes, seconds and miliseconds
    minutes = t // 600
    seconds = (time - minutes*600) // 10
    miliseconds = time % 10
    
    #create resulting string
    if (minutes < 10):
        result += "0" + str(minutes)
    else:
        result += str(minutes)
    result += ":" 
    
    if (seconds < 10):
        result += "0" + str(seconds)
    else:
        result += str(seconds)
    result += "." + str(miliseconds)
       
    return result

def format_score(percents):
    if (percents == 100):
        return "100"
    else:
        return str(percents)[0:4]
  
  
# main logic of the game
def game_handler(stop_time):
    global succeses, attempts, score, string_result
    attempts += 1
    
    if (stop_time % 10 == 0):
        succeses += 1
    
    score = (float(succeses) / float(attempts)) * 100
    string_result = str(succeses) + "/" + str(attempts)
  
  
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    timer.start()
  
def stop_handler():
    if (timer.is_running()):
        timer.stop()
        game_handler(time)
 
def reset_handler():
    global time, succeses, attempts, score, string_result
    time = 0
    succeses = 0
    attempts = 0
    score = 100
    string_result = "0/0"
    timer.stop()

	
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time = time + 1;

# define draw handler
def draw_handler(canvas):
    canvas.draw_text("Your score:", (130, 40), 30, 'Red')
    canvas.draw_text(string_result + "   (" + format_score(score) + "%)", (123, 80), 30, 'Green')
    canvas.draw_text(format_time(time), (90, 210), 70, 'Yellow')
       
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 400, 300, 300)


# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)

start_button_cue = frame.add_label('Press "Start" button to continue a game')
start_button = frame.add_button('Start Timer', start_handler, 300)

stop_button_cue = frame.add_label('Press "Stop" button to make a "shot"')
stop_button = frame.add_button('Stop Timer', stop_handler, 300)

reset_button_cue = frame.add_label('Press "Reset" button to start a new game')
reset_button = frame.add_button('New Game', reset_handler, 300)


# start frame
frame.start()

