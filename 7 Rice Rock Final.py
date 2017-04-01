# To run this program you should use the link provided below:
# http://www.codeskulptor.org
# just put all this document to the left part of the screen 
# and press the "play"-button from the menu area

								# RiceRocks
# Final project of the course. Has several classes, uses basics of sprite animation and
# principles of the most common interaction between the game objects.
								
import simplegui # special framework provided by Coursera
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
MAX_NUM_OF_ROCKS = 10
MAX_LIVES = 5
score = 0
lives = MAX_LIVES
time = 0
started = False


#*********************************************************************************** 
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

#***********************************************************************************     
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

#*********************************************************************************** 
#*********************************************************************************** 
#*********************************************************************************** 
# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , 
							  self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global missiles_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 10 * forward[0], self.vel[1] + 10 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missiles_group.add(a_missile)
    
#***********************************************************************************
#*********************************************************************************** 
#*********************************************************************************** 
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        if self.animated:
            new_position = [(self.image_center[0] + self.age*self.image_size[0]), self.image_center[1]]
            canvas.draw_image(self.image, new_position, self.image_size,
							  self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
							  self.pos, self.image_size, self.angle)
        
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update age
        self.age += 1
        
        # find if sprite is too old
        if (self.age >= self.lifespan):
            return True
        else:
            return False
        
    def collide(self, other):
        distance = dist(self.pos, other.get_position())
        two_radii = self.radius + other.get_radius()
        if (distance < two_radii):
            return True
        else:
            return False

#*********************************************************************************** 
#*********************************************************************************** 
#*********************************************************************************** 
# helper functions
def group_collide(group, sprite):
    global explosion_group
    collision = False
    for element in set(group):
        if (element.collide(sprite)):
            collision = True
            explosion = Sprite(element.get_position(), [0,0], 0, 0, 
							   explosion_image, explosion_info, explosion_sound)
            explosions_group.add(explosion)
            group.remove(element)
    return collision  

def group_group_collide(group1, group2):
    collisions = 0
    for element in set(group1):
        if (group_collide(group2, element)):
            collisions += 1
            group1.discard(element)
    return collisions

def process_group(group, canvas):
    for element in set(group):
        if(element.update()):
            group.remove(element)
        
    for element in group:
        element.draw(canvas)

# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score 
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = MAX_LIVES
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        
        

#*********************************************************************************** 
#*********************************************************************************** 
#*********************************************************************************** 
def draw(canvas):
    global time, started, lives, score
    
    if lives < 1:
        started = False
        for element in set(rocks_group):
            rocks_group.discard(element)
            soundtrack.pause()
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), 
					  [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    if score < 10:
        position_of_score = (WIDTH - 95, 80)
    elif score < 100:
        position_of_score = (WIDTH - 100, 80)
    elif score < 1000:
        position_of_score = (WIDTH - 110, 80)
    elif score < 10000:
        position_of_score = (WIDTH - 115, 80)
    else:
        position_of_score = (WIDTH - 125, 80)
    canvas.draw_text('Lives', (50, 50), 30, 'Lime')
    canvas.draw_text(str(lives), (75, 80), 30, 'Lime')
    canvas.draw_text('Score', (WIDTH - 120, 50), 30, 'Lime')
    canvas.draw_text(str(score), position_of_score, 30, 'Lime')

    # draw ship and sprites
    my_ship.draw(canvas)
    process_group(rocks_group, canvas)
    process_group(missiles_group, canvas)
    process_group(explosions_group, canvas)
    score += 10*group_group_collide(rocks_group, missiles_group)
    
    # update ship and sprites
    my_ship.update()
    if group_collide(rocks_group, my_ship):
        lives -= 1
            
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    

#*********************************************************************************** 
#*********************************************************************************** 
#*********************************************************************************** 
# timer handler that spawns a rock    
def rock_spawner():
    global rocks_group, started
    if (len(rocks_group) < MAX_NUM_OF_ROCKS and started):
        new_position = [random.randrange(50, WIDTH - 50), random.randrange(50, HEIGHT - 50)]
        new_velocity = [(random.random() - 0.5)*4, (random.random() - 0.5)*4]
        new_angle_vel = (random.random() - 0.5)*0.2
        if (dist(new_position, my_ship.get_position()) > 200):
            a_rock = Sprite(new_position, new_velocity, 0, new_angle_vel, 
							asteroid_image, asteroid_info)
            rocks_group.add(a_rock)
        
#*********************************************************************************** 
#*********************************************************************************** 
#*********************************************************************************** 
            
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rocks_group = set()
missiles_group = set()
explosions_group = set()

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

# menu of the game
label1 = frame.add_label('')
label1 = frame.add_label('')
label1 = frame.add_label('************************')
label1 = frame.add_label('-----------Useful info-----------')
label1 = frame.add_label('')
label1 = frame.add_label('************************')
label1 = frame.add_label('')
label1 = frame.add_label('Use arrows to fly around')
label1 = frame.add_label('')
label1 = frame.add_label('Press "Space" for shooting')

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
