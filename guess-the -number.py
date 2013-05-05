# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

# initialize global variables used in your code
message = "Guess the number!"
guess_number = -1
try_count = 7
game_range = 100
secret_number = random.randrange(game_range)
game_output_string = 'New game!'
output_string_color = "Green"    
print "New game. Range is from 0 to 100"
print "Number of remaining guesses is ",try_count

#define helper function
def initiate():
    global secret_number
    global try_count
    if game_range == 100:
        try_count = 7
    else:
        try_count = 10
    secret_number = random.randrange(game_range)    

# define event handlers for control panel
    
def range100():
    # button that changes range to range [0,100) and restarts
    global game_range
    global game_output_string
    global output_string_color
    game_range = 100
    initiate()
    print "\nNew game. Range is from 0 to 100"
    game_output_string = 'New game!'
    output_string_color = "Green"  
    print "Number of remaining guesses is ",try_count
    
    
def range1000():
    # button that changes range to range [0,1000) and restarts
    global game_range
    global game_output_string
    global output_string_color
    game_range = 1000
    initiate()
    print "\nNew game. Range is from 0 to 1000"
    game_output_string = 'New game!'
    output_string_color = "Green" 
    print "Number of remaining guesses is ",try_count

def get_input(guess):
    # main game logic goes here
    global guess_number
    global try_count
    global game_output_string
    global output_string_color
    if int(guess) >= 0 and int(guess) <= game_range:
        guess_number = int(guess)
        try_count -= 1
        if try_count < 0:
            initiate()
            try_count -= 1
            game_output_string = 'Game over'
            output_string_color = "Red"                
        print "\nNumber of remaining guesses is ",try_count    
    else:
        print "Please enter a guess inside the range!"        

def draw(canvas):
    global guess_number
    global secret_number
    global gamer_start
    global game_output_string
    global output_string_color
    global try_count
    
    canvas.draw_text(message, [10,30], 26, "Yellow")
    canvas.draw_text('Range is from 0 to %d   '%game_range, [10,60], 26, "Yellow")
    if secret_number >= 0 and guess_number >= 0:
        if guess_number == secret_number:
            game_output_string = 'Guess was %d, Correct!'%guess_number
            output_string_color = "Green"
            initiate()
        elif guess_number > secret_number:    
            game_output_string = 'Guess was %d, Lower!'%guess_number
            output_string_color = "Blue"
        elif guess_number < secret_number:    
            game_output_string = 'Guess was %d, Higher!'%guess_number
            output_string_color = "Red"

        guess_number = -1

        print game_output_string
    canvas.draw_text(game_output_string, [10,100], 26, output_string_color)
    if try_count > 0:
        canvas.draw_text("Number of remaining guesses is %d"%try_count, [10,150], 16, "Yellow")
    else:
        canvas.draw_text("Number of remaining guesses is %d. Game over!"%try_count, [10,150], 16, "Red")
    
# create frame
frame = simplegui.create_frame("Guess the number", 300, 200)

# register event handlers for control elements
frame.add_button("New game [0,100]", range100)
frame.add_button("New game [0,1000]", range1000)
frame.add_input("Your guess:", get_input, 50)
frame.set_draw_handler(draw)

# start frame
frame.start()

# always remember to check your completed program against the grading rubric
