import pygame
import random
import macchina as m

pygame.init()

#COSTANTI DI PYGAME
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Analisi Semaforo")
waitingTime = 30
FPS = 240

#IMPORT DI IMMAGINI E SCALABILITà DI ESSE
TL_RED_RAW = pygame.image.load("images/traffic_light-red.png")
TL_YELLOW_RAW = pygame.image.load("images/traffic_light-yellow.jpg")
TL_GREEN_RAW = pygame.image.load("images/traffic_light-green.jpg")
TL_RED = pygame.transform.scale(TL_RED_RAW, (20, 60))
TL_YELLOW = pygame.transform.scale(TL_YELLOW_RAW, (20, 60))
TL_GREEN = pygame.transform.scale(TL_GREEN_RAW, (20, 60))

#DEFINIZIONE COLORI DA USARE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,100)
GRAY = (210,210,210)

laneWidth = 100


def drawStreetLimits():
    pygame.draw.line(SCREEN, BLACK, (0,SCREEN_HEIGHT//2-laneWidth-1), (SCREEN_WIDTH,SCREEN_HEIGHT//2-laneWidth-1))
    pygame.draw.line(SCREEN, BLACK, (0,SCREEN_HEIGHT//2+laneWidth+1), (SCREEN_WIDTH,SCREEN_HEIGHT//2+laneWidth+1))
    pygame.draw.line(SCREEN, BLACK, (SCREEN_WIDTH//2-laneWidth-1,0), (SCREEN_WIDTH//2-laneWidth-1,SCREEN_HEIGHT))
    pygame.draw.line(SCREEN, BLACK, (SCREEN_WIDTH//2+laneWidth+1,0), (SCREEN_WIDTH//2+laneWidth+1,SCREEN_HEIGHT))

def drawAsfalto():
    pygame.draw.rect(SCREEN, GRAY, (0,SCREEN_HEIGHT//2-laneWidth, SCREEN_WIDTH,laneWidth*2))
    pygame.draw.rect(SCREEN, GRAY, (SCREEN_WIDTH//2-laneWidth,0,laneWidth*2, SCREEN_HEIGHT))

def drawStreet():
    drawStreetLimits()
    drawAsfalto()

def drawTrafficLight():
    SCREEN.blit(TL_RED, (SCREEN_WIDTH//2- laneWidth - 22, SCREEN_HEIGHT//2- laneWidth - 62))
    SCREEN.blit(TL_GREEN, (SCREEN_WIDTH//2+ laneWidth +2, SCREEN_HEIGHT//2- laneWidth - 62))
    SCREEN.blit(TL_GREEN, (SCREEN_WIDTH//2- laneWidth - 22, SCREEN_HEIGHT//2+ laneWidth +2 ))
    SCREEN.blit(TL_RED, (SCREEN_WIDTH//2+ laneWidth +2, SCREEN_HEIGHT//2+ laneWidth +2 ))

def drawBackground():
    SCREEN.fill(WHITE)
    drawStreet()
    drawTrafficLight()

def drawVeicles():
    global listAuto
    for c in listAuto:
        c.drawCar(SCREEN)

def updateScreen():
    pygame.display.flip()
    pygame.time.delay(waitingTime)
    pygame.time.Clock().tick(FPS)


def aggiorna():
    drawBackground()
    drawVeicles()
    updateScreen()
    
def creaAuto():
    global listAuto
    c = m.Macchina(BLACK)
    listAuto.append(c)
    


def running():
    global listAuto
    count = 0
    p = 1
    listAuto = []
    drawBackground()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        count += 1
        if count // 20 == p:
            p += 1
            creaAuto()
        for c in listAuto:
            c.move()

        aggiorna()





if __name__ == "__main__":
    running()

