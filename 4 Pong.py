# To run this program you should use the link provided below:
# http://www.codeskulptor.org
# just put all this document to the left part of the screen 
# and press the "play"-button from the menu area

		# Implementation of the classic arcade game Pong
# Control: 
# W, S 		for Player 1
# Up, Down 	for Player 2
		
import simplegui # special framework provided by Coursera
import random

# initialize globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 90
PAD_SPEED = 5
BALL_RADIUS = 20
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_pos = WIDTH / 2
paddle2_pos = HEIGHT / 2

paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [1,1]


# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]  
    ball_vel[0] = float(random.randrange(120, 240)) / 60
    ball_vel[1] = - float(random.randrange(60, 180)) / 60
    if (direction == LEFT):
        ball_vel[0] *= (-1)
	

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0	
    side = random.randrange(0,2)
    
    if (side == 1):
        spawn_ball(LEFT)
    else: 
        spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 2 - 100, 70), 60, 'Yellow')
    canvas.draw_text(str(score2), (WIDTH / 2 + 70, 70), 60, 'Yellow') 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if (ball_pos[1] - BALL_RADIUS < 0):
        ball_vel[1] *= (-1)
    if (ball_pos[1] + BALL_RADIUS > HEIGHT):
        ball_vel[1] *= (-1)
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 
                
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'Red', 'Red')
    
    # update paddle's vertical position, keep paddle on the screen
    if((paddle1_pos - HALF_PAD_HEIGHT + paddle1_vel >= 0) and 
	(paddle1_pos + HALF_PAD_HEIGHT + paddle1_vel <= HEIGHT)):
        paddle1_pos += paddle1_vel 
    
    if((paddle2_pos - HALF_PAD_HEIGHT + paddle2_vel >= 0) and 
	(paddle2_pos + HALF_PAD_HEIGHT + paddle2_vel <= HEIGHT)):
        paddle2_pos += paddle2_vel 
    
    # draw paddles
    left_pad = [[0, paddle1_pos + HALF_PAD_HEIGHT], 
				[0, paddle1_pos - HALF_PAD_HEIGHT], 
				[PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
				[PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT]]
	
    right_pad = [[WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], 
			 	 [WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
				 [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
				 [WIDTH, paddle2_pos + HALF_PAD_HEIGHT]]
				 
    canvas.draw_polygon(left_pad, 1, 'Black', 'Black')
    canvas.draw_polygon(right_pad, 1, 'Black', 'Black')
    
    
    # determine whether paddle and ball collide 
    ball_upper_left = (ball_pos[1] + 10) < (paddle1_pos - HALF_PAD_HEIGHT)
    ball_lower_left = (ball_pos[1] - 10) > (paddle1_pos + HALF_PAD_HEIGHT)
    ball_upper_right = (ball_pos[1] + 10) < (paddle2_pos - HALF_PAD_HEIGHT)
    ball_lower_right = (ball_pos[1] - 10) > (paddle2_pos + HALF_PAD_HEIGHT)
	
    if (ball_pos[0] - BALL_RADIUS - PAD_WIDTH < 0):
        if (ball_upper_left or ball_lower_left):
            score2 += 1
            spawn_ball(RIGHT)
        else:
            ball_vel[1] *= (1.05)
            ball_vel[0] *= (-1.05)
        
    if (ball_pos[0] + BALL_RADIUS + PAD_WIDTH > WIDTH):
        if (ball_upper_right or ball_lower_right):
            score1 += 1
            spawn_ball(LEFT)
            
        else:
            ball_vel[1] *= (1.05)
            ball_vel[0] *= (-1.05)
    
def keydown(key):
    global paddle1_vel, paddle2_vel
	
	# player 1 control
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= PAD_SPEED
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += PAD_SPEED
		
    # player 2 control
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= PAD_SPEED
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += PAD_SPEED
   
def keyup(key):
    global paddle1_vel, paddle2_vel
	
	# player 1 control
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += PAD_SPEED
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel -= PAD_SPEED
    
	# player 2 control
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel += PAD_SPEED
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel -= PAD_SPEED


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background('Green')

# draw a menu of the game
label1 = frame.add_label("**********************")
label1 = frame.add_label("Player 1:")
label1 = frame.add_label("Up   -  'W'")
label1 = frame.add_label("Down -  'S'")
label1 = frame.add_label("")
label1 = frame.add_label("Player 2:")
label1 = frame.add_label("Standart arrows")
label1 = frame.add_label("")
label1 = frame.add_label("**********************")
label1 = frame.add_label("")
button1 = frame.add_button('New Game', new_game, 200)

# events support
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
