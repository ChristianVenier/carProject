import pygame
import random

global laneWidth

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
laneWidth = 100

class Macchina:
    
    def __init__(self,  color):
        startKey = random.randint(1,8)
        self.width = 40
        self.height = 15
        start = {
        1 : [0, SCREEN_HEIGHT//2 + laneWidth//4 - self.height//2],
        2 : [0, SCREEN_HEIGHT//2 + laneWidth//4*3 - self.height//2],
        3 : [SCREEN_WIDTH//2+ laneWidth//4 - self.height, SCREEN_HEIGHT-self.width],
        4 : [SCREEN_WIDTH//2+ laneWidth//4*3 - self.height//2, SCREEN_HEIGHT-self.width],
        5 : [SCREEN_WIDTH - self.width, SCREEN_HEIGHT//2 - laneWidth//4 - self.height//2],
        6 : [SCREEN_WIDTH - self.width, SCREEN_HEIGHT//2 - laneWidth//4*3 - self.height//2],
        7 : [SCREEN_WIDTH//2 - laneWidth//4 - self.height//2,0],
        8 : [SCREEN_WIDTH//2 - laneWidth//4*3 - self.height//2,0],
    }
        self.pos = start[startKey]
        self.color = color
        if startKey == 1 or startKey == 2:
            self.dirnx = 1
            self.dirny = 0
        elif startKey == 3 or startKey == 4:
            self.dirnx = 0
            self.dirny = -1
        elif startKey == 5 or startKey == 6:
            self.dirnx = -1
            self.dirny = 0
        elif startKey == 7 or startKey == 8:
            self.dirnx = 0
            self.dirny = 1

    def createVisibleArea(self):
        pass

    def move(self):
        self.pos[0] += self.dirnx
        self.pos[1] += self.dirny

    
    def drawCar(self, surface):
        if self.dirny == 0:
            self.horizontalCar(surface) 
        else:
            self.verticalCar(surface)

    def horizontalCar(self,surface):
        pygame.draw.rect(surface, self.color, (self.pos[0], self.pos[1], self.width, self.height))

    def verticalCar(self,surface):
        pygame.draw.rect(surface, self.color, (self.pos[0], self.pos[1], self.height, self.width))
        
        

    def checkTrafficLight(self):
        pass

    def isCrashed():
        pass