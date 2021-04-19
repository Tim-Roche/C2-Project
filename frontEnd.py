import pygame
from pygame.locals import *
from controlModel import controlModel
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

pygame.init()
screen = pygame.display.set_mode((1200, 1200))
clock = pygame.time.Clock()
pygame.display.set_caption("C2 Final Project")
font = pygame.font.SysFont('Arial', 25)


#fig = plt.figure()
FRAMES_SECOND = 60

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
SIZE = 75

#Game Settings
columns = 3
rows = 3
speed = 0.5 #time between generations (in seconds)

#Game Variables
currentGen = 0
count = 0
start = 0



c = controlModel(columns, rows)
s = c.state

#ax1 = fig.add_subplot(1,1,1)

def gradient(percent):
    percent = round(percent,2)
    percent = min(percent,1)
    red = percent*255
    green = (1 - percent)*255
    return((int(red), int(green), 0))

def gradientBlue(percent):
    percent = round(percent,2)
    percent = min(percent,1)
    blue = percent*255
    #print(percent, blue)
    return((0, 0, blue))

def convertToGrid(metric, r=0):
    metric = [round(m,r) for m in metric]
    output = np.reshape(metric, (columns,rows), order="F")
    return(output)

def convertToGradient(metric, color="normal"):
    g = [gradient(m) for m in metric]
    if color == "blue":
        g = [gradientBlue(m) for m in metric]
    return(g) 


def animate(i):
    c.tick_time()
    m = s.get_region(2,2)
    ax1.clear()
    ax1.plot(m.time, m.infected, label='Infected')
    ax1.plot(m.time, m.susceptible, label='Susceptible')
    ax1.plot(m.time, m.recovered, label='Recovered')
    ax1.plot(m.time, m.dead, label='Dead')
    ax1.plot(m.time, m.vaccinated, label='Fully Vaccinated')
    ax1.plot(m.time, m.susHR, label='High Risk Population')
    ax1.title.set_text("Region 1")
    ax1.legend()


def main():
    notComplete = True
    debug = False
    done = False

    while not done:
        if notComplete:
            notComplete = c.tick_time()

        reports = c.getCurrentRegionReports()
        infected = c.getPercentageInfections(reports)
        highRisk = c.getPercentageHighRisk(reports)
        vaccinated = c.getPercentVaccinated(reports)
        R0 = c.getR0(reports)




ani = animation.FuncAnimation(fig, animate, interval=FRAMES_SECOND)
plt.show()
main()



