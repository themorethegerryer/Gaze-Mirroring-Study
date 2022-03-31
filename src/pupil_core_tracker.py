import zmq
import numpy as np
from eye_animation import draw_eyes

# Gaze Metrics
#   length of eye contact (s)
#   length of gaze aversion (s)
#   angle of gaze aversion (theta)
#   blinking? - hard to mimic, probably not gonna use
#   frequency of gaze aversion (/min)