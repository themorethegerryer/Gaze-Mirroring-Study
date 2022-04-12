import pygame
import numpy as np
import time

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

if __name__ == "__main__":
    robot = Robot()
    
    while True:
        r = np.random.uniform()
        theta = np.random.uniform(low=-np.pi, high=np.pi)
        print("Eye changes " + str(r) + " - " + str(theta))
        robot.update(theta,r)
        time.sleep(1.0)