import zmq
import msgpack
import pickle
import os
import signal
from sys import exit
import numpy as np
import eye_animation
import time

# Gaze Metrics
#   length of eye contact (s)
#   length of gaze aversion (s)
#   angle of gaze aversion (theta)
#   frequency of blinks (/min)
#   frequency of gaze aversion (/min)

def warp2pi(angle_rad):
    """
    Warps an angle in [-pi, pi]. Used in the update step.

    \param angle_rad Input angle in radius
    \return angle_rad_warped Warped angle to [-\pi, \pi].
    """
    return (angle_rad + np.pi) % (2*np.pi) - np.pi

class GazeModel:
    def __init__(self, subject_name="Default Defaulterson", trial=0):
        self.path2models = "../models/"
        self.filename = subject_name+"-"+str(trial)+".pkl"
        
        self.model = {
            "eye_contact_length" : 0, # seconds
            "gaze_aversion_length" : 0, # seconds
            "gaze_aversion_theta" : 0, # theta [-\pi, \pi]
            "gaze_aversion_freq" : 0, # times/min
            "blink_freq" : 0 # times/min
            }
        
        # If subject model already exists, load it in. Otherwise, create fresh
        if os.path.exists(self.path2models+self.filename):
            with open(self.path2models+self.filename,'wb') as fp:
                self.model = pickle.load(fp)
    
    def save_model(self):
        with open(self.path2models+self.filename,'wb') as fp:
            pickle.dump(self.model, fp)
            
gaze_model = None

def handler(signum, frame):
    if gaze_model is not None:
        print("Test terminated --- saving model", flush=True)
        gaze_model.save_model()
    else:
        print("No gaze model created")
    exit(1)
    
signal.signal(signal.SIGINT,handler)

    
if __name__ == "__main__":
    robot = eye_animation.Robot()
        
    ctx = zmq.Context()
    # The REQ talks to Pupil remote and receives the session unique IPC SUB PORT
    pupil_remote = ctx.socket(zmq.REQ)
    
    ip = 'localhost'  # If you talk to a different machine use its IP.
    port = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.
    
    pupil_remote.connect(f'tcp://{ip}:{port}')
    
    # Request 'SUB_PORT' for reading data
    pupil_remote.send_string('SUB_PORT')
    sub_port = pupil_remote.recv_string()
    
    # Request 'PUB_PORT' for writing data
    pupil_remote.send_string('PUB_PORT')
    pub_port = pupil_remote.recv_string()
    
    # Assumes `sub_port` to be set to the current subscription port
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect(f'tcp://{ip}:{sub_port}')
    # subscriber.subscribe('gaze.')  # receive all gaze messages
    subscriber.subscribe('fixations')
    subscriber.subscribe('blinks')
    
    while True:
        topic, payload = subscriber.recv_multipart()
        message = msgpack.loads(payload)
        print(f"{topic}: {message}")
        # print(str(topic))
        if str(topic) == "b\'fixations\'":
            print(message['norm_pos'])
            x = message['norm_pos'][0]
            y = message['norm_pos'][1]
            theta = np.arctan2(y,x)
            r = np.sqrt(np.square(x)+np.square(y))
            print(theta,r)
            robot.update(theta,r)
        elif str(topic) == "b\'gaze.3d.1.\'":
            print(message['norm_pos'])
            x = message['norm_pos'][0]
            y = message['norm_pos'][1]
            theta = np.arctan2(y,x)
            r = np.sqrt(np.square(x)+np.square(y))
            print(theta,r)
            robot.update(theta,r)
        elif str(topic) == "b\'blinks\'":
            pass