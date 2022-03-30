import numpy as np
import pyglet

'''
draw_eyes(theta,r)
theta: [0,2*pi] angle the pupils in polar coordinates (0 is pupils right, looking left)
r: [0,1] pupil distance from center (normalized where 0 is looking straight, 1 is at edge of eye)

This function animates the robot's eyes based on the input polar cordinates of the pupils (using pyglet for animation).
For simplicity, this animation assumes both pupils are moving and looking in the same direction.

return: None
'''
def draw_eyes(theta,r):
    pass


'''
blink() [Optional, we may not need this, or it may be easier to include it in draw_eyes]

This function, when called, will blink the robot's eyes

return: None
'''
def blink():
    pass