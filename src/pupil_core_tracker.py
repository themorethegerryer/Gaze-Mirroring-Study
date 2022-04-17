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

gaze_model = None
robot = None
eye_contact_lens = []
gaze_aversion_lens = []
gaze_aversion_thetas = []
gaze_aversions = 0
blinks = 0

blink_thresh = 1 #seconds
blink_time = 0.0
eye_contact_time = 0.0
averted_gaze_time = 0.0
start_time = 0.0
total_time = 0.0

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
            "eye_contact_length" : 3.3, # seconds
            "gaze_aversion_length" : 0.7, # seconds
            "gaze_aversion_theta" : np.pi/3, # theta [-\pi, \pi]
            "gaze_aversion_r" : 0.5, # normalize [0,1]
            "gaze_aversion_freq" : 0.0, # times/min
            "blink_freq" : 18.0 # times/min
            }
        
        # If subject model already exists, load it in. Otherwise, create fresh
        if os.path.exists(self.path2models+self.filename):
            with open(self.path2models+self.filename,'rb') as fp:
                self.model = pickle.load(fp)
    
    def save_model(self):
        with open(self.path2models+self.filename,'wb') as fp:
            pickle.dump(self.model, fp)
            

def handler(signum, frame):
    if gaze_model is not None:
        robot.kill()
        print("Test terminated --- building model", flush=True)
        total_time = time.perf_counter()-start_time
        gaze_model.model['blink_freq'] = blinks/(total_time/60)
        
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
    subscriber.subscribe('gaze.')  # receive all gaze messages
    subscriber.subscribe('fixations')
    subscriber.subscribe('blinks')
    
    # subject_name = input("Name of subject:\t")
    # trial = input("Trial:\t")
    # gaze_model = GazeModel(subject_name=subject_name, trial=trial)
    gaze_model = GazeModel()
    
    start_time = time.perf_counter()
    while True:
        topic, payload = subscriber.recv_multipart()
        message = msgpack.loads(payload)
        # print(f"{topic}: {message}")
        # print(str(topic))
        if str(topic) == "b\'fixations\'":
            print(message['norm_pos'])
            x = (message['norm_pos'][0]*2)-1
            y = (message['norm_pos'][1]*2)-1
            theta = np.arctan2(y,x)
            r = np.sqrt(np.square(x)+np.square(y))
            print("Fixation:",theta,r)
            # robot.update(theta,r)
        elif str(topic) == "b\'gaze.3d.1.\'":
            print(message['norm_pos'])
            if np.linalg.norm(message['norm_pos']) < 10:
                x = (message['norm_pos'][0]*2)-1
                y = (message['norm_pos'][1]*2)-1
                theta = np.arctan2(y,x)
                r = np.sqrt(np.square(x)+np.square(y))
                print("Gaze:", theta,r)
                robot.update(theta,r)
        elif str(topic) == "b\'blinks\'":
            if time.perf_counter() - blink_time > blink_thresh:
                blinks += 1
                blink_time = time.perf_counter()