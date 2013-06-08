# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0
started = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])
game_speed = 1

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
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

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
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = [0,0]
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.thrust == True:
            canvas.draw_image(self.image, [self.image_center[0] + 90, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = self.pos[0] + self.vel[0] % width
        self.pos[1] = self.pos[1] + self.vel[1] % height
        self.pos[0] = self.pos[0] % width
        self.pos[1] = self.pos[1] % height
        # the following two lines are to induce friction, which caps maximum velocity 
        # and also causes ship to slowly stop by itself when thrusters are off
        self.vel[0] *= .99
        self.vel[1] *= .99
        if self.thrust == True:
            self.forward = angle_to_vector(self.angle)
            self.vel[0] += self.forward[0] * .2
            self.vel[1] += self.forward[1] * .2
        
    def keydown(self,key):
        ang_vel = .09
        if key == simplegui.KEY_MAP['left']:
            self.angle_vel = - ang_vel
        elif key == simplegui.KEY_MAP['right']:
            self.angle_vel = ang_vel
        elif key == simplegui.KEY_MAP['up']:
            self.thrust = True
            if self.thrust == True:
                sound = ship_thrust_sound
                sound.play()
        elif key == simplegui.KEY_MAP['space']:
            self.shoot()
            
    def keyup(self,key):
        angle_vel = 0
        if key == simplegui.KEY_MAP['right']:
            my_ship.angle_vel = angle_vel
        elif key == simplegui.KEY_MAP['left']:
            my_ship.angle_vel = angle_vel
        elif key == simplegui.KEY_MAP['up']:
            self.thrust = False
            if self.thrust == False:
                self.forward = [0,0]
                sound = ship_thrust_sound
                sound.pause()
                
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))

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
        self.speed = 1
        if sound:
            sound.rewind()
            sound.play()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_vel(self):
        return self.vel
    
    def draw(self, canvas):
        global started
        if started:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]),self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        global score, game_speed
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % height
        if self.image == asteroid_image and score >= 100:
            #self.speed = (score * 1.01) / score
            game_speed = (score * 1.02 / score)
            self.vel[0] *= .983
            self.vel[1] *= .983
        self.vel = [self.vel[0] * game_speed, self.vel[1] * game_speed]
        self.angle += self.angle_vel
        self.age += 1
        if self.age < self.lifespan:
            return True
        else:
            return False
        
    def collide(self, other_object):
        other_pos = other_object.get_position()
        other_rad = other_object.get_radius()
        distance = dist(self.pos,other_pos)
        if distance < self.radius + other_rad:
            return True
        else:
            return False
        
def draw(canvas):
    global time, lives, started, rock_group
    
    # animate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])
    canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [2*wtime, size[1]], 
                                [1.25*wtime, height/2], [2.5*wtime, height])
    
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group,canvas)
    process_sprite_group(missile_group,canvas)
    process_sprite_group(explosion_group,canvas)
    
    # update ship and sprites
    my_ship.update()
    # missile_group.update()
    if group_collide(rock_group, my_ship) > 0:
        lives -= 1
    group_group_collide(missile_group, rock_group)
    
    # end of game handling
    if lives == 0:
        started = False
        rock_group = set([])
        timer.stop()
        soundtrack.rewind()
        
    # draw score and lives
    canvas.draw_text("Lives: " + str(lives), (width * 0.05, height * 0.1), 24, "White")
    canvas.draw_text("Score: " + str(score), (width * 0.8, height * 0.1), 24, "White")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [width/2, height/2], 
                          splash_info.get_size())
    
# draw splash screen at launch and after each game ends
def click(pos):
    global started, lives
    center = [width / 2, height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        timer.start()
        rock_spawner()
        soundtrack.play()

# feeds draw handler for sprite groups
def process_sprite_group(group_name, canvas_name):
    for sprite in group_name:
        remove_sprite = set([])
        sprite.draw(canvas_name)
        if sprite.update() == False:
            remove_sprite.add(sprite)
        group_name.difference_update(remove_sprite)
        
# removes sprites upon collision with ship
def group_collide(group, other_object):
    remove_set = set([])
    for sprite in group:
        if sprite.collide(other_object) == True:
            explosion_group.add(Sprite(sprite.get_position(), sprite.get_vel(), 0, 0, explosion_image, explosion_info))
            remove_set.add(sprite)
        group.difference_update(remove_set)
    if len(remove_set) > 0:
        return True

# handles collisions between missiles and rocks
def group_group_collide(group1, group2):
    remove_set = set([])
    global score
    for sprite in group1:
        if group_collide(group2,sprite) == True:
            score += 10
            remove_set.add(sprite)
        group1.difference_update(remove_set)
        
# timer handler that spawns rock sprites
def rock_spawner():
    global rock_group
    rock_pos = [width * random.random(), height * random.random()]
    rock_vel = [random.random() * 3 - 1.5,random.random() * 3 - 1.5]
    distance = dist(rock_pos, my_ship.get_position())
    if started:
        if len(rock_group) < 12:
            if distance > my_ship.get_radius() + asteroid_info.get_radius() + 60:
                rock_group.add(Sprite(rock_pos, rock_vel, 0, (random.random() - .5) / 8, asteroid_image, asteroid_info))
    
def key_down(key):
    my_ship.keydown(key)
    
def key_up(key):
    my_ship.keyup(key)
    
# frame initialization
frame = simplegui.create_frame("Asteroids", width, height)

# ship and sprite initialization
my_ship = Ship([width / 2, height / 2], [0, 0], 1.5 * math.pi, ship_image, ship_info)
rock_group.add(Sprite([width * random.random(), height * random.random()], [random.random() * 3 - 1.5,random.random() * 3 - 1.5], 0, (random.random() - .5) / 8, asteroid_image, asteroid_info))
missile_group.add(Sprite([2 * width / 3, 2 * height / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound))

# handler registration
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()