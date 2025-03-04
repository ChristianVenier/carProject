import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Analisi Semaforo")
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
background = pygame.image.load("images/background.png")

def inizializza():
    SCREEN.blit(background, (10,10))

def aggiorna():
    pygame.display.flip()



def running():
    inizializza()
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        aggiorna()
        




if __name__ == "__main__":
    running()

