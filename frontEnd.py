import pygame
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
GRAY = (112,128,144)
SLATE_GRAY = (47,79,79)
SILVER = (192,192,192)
ROYAL_BLUE = (65,105,225)

#Grid Layout Settings
X_PADDING = 0
Y_PADDING = 0
TITLE_SIZE = 15 #NEEDS to be smaller than TITLE_PADDING
TITLE_PADDING = 30
SIZE = 100

#Game Settings
yVal = 2
xVal = 2
speed = 0.5 #time between generations (in seconds)

#Game Variables
currentGen = 0
count = 0
start = 0

#Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((800, 750))
clock = pygame.time.Clock()
pygame.display.set_caption("C2 Final Project")

def gradient(percent):
    percent = percent
    green = percent*255
    red = (1 - percent)*255
    return((red, green, 0))

def main():
    done = False
    while not done:
        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #Update Board
        area = [[gradient(0.1), gradient(0.3)],[gradient(0.6), gradient(0.8)]]
        for y in range(0,yVal):
            for x in range(0,xVal):
                value = area[y][x]
                color = value
                finalX = (x*(SIZE+X_PADDING))
                finalY = (y*(SIZE+Y_PADDING)) + TITLE_PADDING
                pygame.draw.rect(screen, color, pygame.Rect(finalX, finalY, SIZE, SIZE))

        #Refresh
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()


