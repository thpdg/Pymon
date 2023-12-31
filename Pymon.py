# Plays Simon on the Interstate 75 32x32 board (But could probably work on any square display)
# Draw blank board
# Start with a sequence? Or generate on fly
# Light first light and add to array
# Wait for player press
# Play first light and add one more
# Keep having player do pattern, add a light, play pattern, repeat

import random
import time
import math
from pimoroni_i2c import PimoroniI2C
from pimoroni import HEADER_I2C_PINS  # or PICO_EXPLORER_I2C_PINS or HEADER_I2C_PINS
from breakout_encoder_wheel import BreakoutEncoderWheel, UP, DOWN, LEFT, RIGHT, CENTRE, NUM_LEDS
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_32X32

# Setup graphics for i75 LED board
i75 = Interstate75(display=DISPLAY_INTERSTATE75_32X32)
graphics = i75.display
width = i75.width
height = i75.height

# BRight Segments
WHITE = graphics.create_pen(255, 255, 255)
BLUE = graphics.create_pen(0, 0, 255)
RED = graphics.create_pen(255, 0, 0)
BLACK = graphics.create_pen(0,0,0)
YELLOW = graphics.create_pen(237,213,38)
GREEN = graphics.create_pen(0,255,0)

# Dim Segments
DIM_BLUE = graphics.create_pen(0, 0, 128)
DIM_RED = graphics.create_pen(128, 0, 0)
DIM_YELLOW = graphics.create_pen(118,107,38)
DIM_GREEN = graphics.create_pen(0,128,0)

# Draw a segment
def draw_wedge(qx,qy,fg,bg,radius, core_radius):
    graphics.set_clip(qx*17,qy*17, qx+15, qy+15)
    graphics.set_pen(fg)
    graphics.circle(qx+15, qy+15, radius)
    graphics.set_pen(bg)
    graphics.circle(qx+15, qy+15, core_radius)
    graphics.remove_clip()
    print("Drawn")
    pass

# Wrapper to make it easier to work in game wedges
#  Python 3.10 match statement doesn't appear to be implemented in this version of Micropython
def draw_quad(quad,lit):
    outer_radius = 14
    inner_radius = 5
    if quad == 0:
        draw_wedge(0,0, GREEN if lit == True else DIM_GREEN, BLACK, outer_radius,inner_radius)
    if quad == 1:
        draw_wedge(0,1, YELLOW if lit == True else DIM_YELLOW, BLACK, outer_radius,inner_radius)
    if quad == 2:
        draw_wedge(1,0, RED if lit == True else DIM_RED, BLACK, outer_radius,inner_radius)
    if quad == 3:
        draw_wedge(1,1, BLUE if lit == True else DIM_BLUE, BLACK, outer_radius,inner_radius)

graphics.remove_clip()
graphics.set_pen(BLACK)
graphics.clear()

# Initialize Board
draw_quad(0,False)
draw_quad(1,False)
draw_quad(2,False)
draw_quad(3,False)
i75.update()
time.sleep(2)

Current_Game = []
current_step = 0
current_step_pause = 1.0

while True:
    # Add a step
    Current_Game.append(random.randrange(0,4))
    
    # Playback steps
    for x in Current_Game:
        draw_quad(x,True)
        i75.update()
        time.sleep(current_step_pause)
        draw_quad(x,False)
        i75.update()
        time.sleep(current_step_pause)
    
    current_step_pause = current_step_pause if current_step_pause < 0.2 else current_step_pause - 0.1
    print("Step is now " + str(current_step_pause))
    print("Array is " + str(Current_Game))
    time.sleep(3)
    
    # Display happy indicator?

i75.update()
