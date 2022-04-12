import math
import pyglet


'''
draw_eyes(theta,r)
theta: [0,2*pi] angle the pupils in polar coordinates (0 is pupils right, looking left)
r: [0,1] pupil distance from center (normalized where 0 is looking straight, 1 is at edge of eye)

This function animates the robot's eyes based on the input polar cordinates of the pupils (using pyglet for animation).
For simplicity, this animation assumes both pupils are moving and looking in the same direction.

return: None
'''
# all the way to the right: x = 309, y = 395 (theta = 0, 2pi)
# all the way to the left: x = 196, y = 395 (theta = pi)
# all the way up: x = 253, y = 452 (theta = pi/2)
# all the way down: x = 253, y = 341 (theta = 3pi/2)

# Default position
window = pyglet.window.Window(1000,773)

pic = pyglet.resource.image('robotface.png')
sprite = pyglet.sprite.Sprite(pic, x = 0, y = 0)

pupil = pyglet.resource.image('pupils.png')
sprite2 = pyglet.sprite.Sprite(pupil, x = 253, y = 395)


@window.event
def on_draw():
    window.clear()
    sprite.draw()
    sprite2.draw()

#sprite2.update(x = (253 + 1 * math.cos(0)), y = (395 + 1 * math.sin(0)))


pyglet.app.run()

def draw_eyes(theta,r):
    pass


'''
blink() [Optional, we may not need this, or it may be easier to include it in draw_eyes]

This function, when called, will blink the robot's eyes

return: None
'''
def blink():
    pass