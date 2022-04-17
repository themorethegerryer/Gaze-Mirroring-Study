import pygame
import numpy as np
import time
import pickle

dis_width = 1000
dis_height = 773

eyes_at_center = (253, 245)
eye_radius = 56

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
robot_gray = (121, 151, 179)

time_interval = 0.1

class Robot:
    def __init__(self):
        pygame.init()
 
        self.dis = pygame.display.set_mode((dis_width, dis_height))
        pygame.display.set_caption('Robot')
        
        self.robotface = pygame.image.load('robotface.png')
        self.pupils = pygame.image.load('pupils.png')
        
        self.dis.fill(blue)
        self.dis.blit(self.robotface, (0,0))
        self.dis.blit(self.pupils,eyes_at_center)

    def update(self, theta, r):
        self.dis.fill(blue)
        self.dis.blit(self.robotface, (0,0))
        self.dis.blit(self.pupils,((eyes_at_center[0] + eye_radius * r * np.cos(-theta)),(eyes_at_center[1] + eye_radius * r * np.sin(-theta))))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
    def kill(self):
        pygame.quit()

def open_model(subject_name="Default Defaulterson", trial=0):
    filename = subject_name+"-"+str(trial)+".pkl"
    with open("../models/"+filename,'rb') as fp:
                model = pickle.load(fp)
    return model

if __name__ == "__main__":
    robot = Robot()
    # subject_name = input("Name of subject:\t")
    # trial = input("Trial:\t")
    # gaze_model = open_model(subject_name=subject_name, trial=trial)
    gaze_model = open_model()
    print(gaze_model)
    
    # blink_prob = gaze_model.model['blink_freq']/(60/time_interval)
    gaze_averted = True
    timer = 0.0
    # blinking = False
    while True:
        # if not blinking:
        #     do_blink = (blink_prob < np.random.uniform())
        #     if do_blink:
        #         robot.blink()
        timer += time_interval
        if not gaze_averted:
            # print("Eye contact")
            robot.update(0,0)
            if timer > gaze_model["eye_contact_length"]:
                gaze_averted = True
                timer = 0.0
        else:
            # print("Gaze Averted")
            robot.update(gaze_model["gaze_aversion_theta"], gaze_model["gaze_aversion_r"])
            if timer > gaze_model["gaze_aversion_length"]:
                gaze_averted = False
                timer = 0.0
                
        time.sleep(time_interval)
    
    # Random eye movement test
    # while True:
    #     r = np.random.uniform()
    #     theta = np.random.uniform(low=-np.pi, high=np.pi)
    #     print("Eye changes " + str(r) + " - " + str(theta))
    #     robot.update(theta,r)
    #     time.sleep(1.0)