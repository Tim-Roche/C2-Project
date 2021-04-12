import pygame
from pygame.locals import *
from controlModel import controlModel
import numpy as np

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
columns = 10
rows = 10
speed = 0.5 #time between generations (in seconds)

#Game Variables
currentGen = 0
count = 0
start = 0

#Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((1200, 1200))
clock = pygame.time.Clock()
pygame.display.set_caption("C2 Final Project")
font = pygame.font.SysFont('Arial', 25)

def gradient(percent):
    percent = round(percent,2)
    percent = min(percent,1)
    red = percent*255
    green = (1 - percent)*255
    return((int(red), int(green), 0))

def convertToGrid(metric, r=0):
    metric = [round(m,r) for m in metric]
    output = np.reshape(metric, (columns,rows), order="F")
    return(output)

def convertToGradient(metric):
    g = [gradient(m) for m in metric]
    return(g) 

def main():
    c = controlModel(columns, rows)
    notComplete = True

    done = False
    while not done:
        if notComplete:
            notComplete = c.tick_time()

        reports = c.getCurrentRegionReports()
        infected = c.getPercentageInfections(reports)
        highRisk = c.getPercentageHighRisk(reports)
        R0 = c.getR0(reports)

        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        textData = convertToGrid(highRisk, r=2)
        print(textData)
        #print(textData)
        #Update Board
        area = convertToGradient(highRisk)
        for y in range(0,columns):
            for x in range(0,rows):
                color = area[x*y + y]
                finalX = (x*(SIZE+X_PADDING))
                finalY = (y*(SIZE+Y_PADDING)) + TITLE_PADDING
                pygame.draw.rect(screen, color, pygame.Rect(finalX, finalY, SIZE, SIZE))

                midX = (finalX + SIZE/2) 
                midY = (finalY + SIZE/2) 
                screen.blit(font.render(str(textData[y][x]), True, WHITE), (midX, midY))

        #Refresh
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()


