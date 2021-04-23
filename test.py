import pygame, sys
from pygame.locals import *
import numpy as np
import numpy 
import matplotlib
import matplotlib.animation as animation
from controlModel import controlModel
import Report
import sys

algorithm = "weighted"
if(len(sys.argv) > 1):
    if(sys.argv[1] == "even"):
        algorithm = "even"
    elif(sys.argv[1] == "weighted"):
        algorithm = "weighted"
    else:
        print("Unknown Input")
        print("Try 'even' or 'weighted'")
        exit(0)


matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg

#Game Settings
columns = 3
rows = 3

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
color = (255,255,255)
# light shade of the button
color_light = (170,170,170)
# dark shade of the button
color_dark = (100,100,100)
  

fig = plt.figure(figsize=[8, 4])
statePlot = fig.add_subplot(111)
stateCanvas = agg.FigureCanvasAgg(fig)

fig2 = plt.figure(figsize=[10, 5])
pvMap = fig2.add_subplot(1,3,2)
pprMap = fig2.add_subplot(1,3,1)
infMap = fig2.add_subplot(1,3,3)
#hrMap = fig2.add_subplot(1,3,3)

#R0Map = fig2.add_subplot(1,4,4)

heatCanvas = agg.FigureCanvasAgg(fig2)



def writeToScreen(canvas):
   canvas.draw()
   renderer = canvas.get_renderer()

   raw_data = renderer.tostring_rgb()
   size = canvas.get_width_height()
   
   return pygame.image.fromstring(raw_data, size, "RGB")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1025, 700))
font = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont(None, 50)
# defining a font
smallfont = pygame.font.SysFont('Corbel',35)

pygame.display.set_caption('C2 Final Project')

totalInfected = []
totalSusceptible = []
totalRecovered = []
totalDay = []
totalDead = []
totalVaccinated = []
totalSusHR = []
weights = [2,0,2,19]
c = controlModel(columns, rows, weights)
s = c.state

count = 1
a = []

def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    if not isinstance(data, (list, np.ndarray)):
            data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

def plotStateOverview(reports, stateReport):
    totalInfected.append(stateReport.get_infected()/1000)
    totalDay.append(stateReport.get_day())
    totalSusceptible.append(stateReport.get_susceptible()/1000)
    totalRecovered.append(stateReport.get_recovered()/1000)
    totalDead.append(stateReport.get_dead()/1000)
    totalVaccinated.append(stateReport.get_vaccinated()/1000)
    totalSusHR.append(stateReport.get_r() * stateReport.get_susceptible()/1000)
    statePlot.clear()
    statePlot.set_title("State Level Pandemic Dashboard")
    statePlot.set_xlabel('Days')
    statePlot.set_ylabel('People/1000')
    statePlot.plot(totalDay, totalInfected, label='Infected')
    statePlot.plot(totalDay, totalSusceptible, label='Susceptible')
    statePlot.plot(totalDay, totalRecovered, label='Recovered')
    statePlot.plot(totalDay, totalDead, label='Dead')
    statePlot.plot(totalDay, totalVaccinated, label='Fully Vaccinated')
    statePlot.plot(totalDay, totalSusHR, label='High Risk Population')
    statePlot.legend()
    surf = writeToScreen(stateCanvas)
    return(surf)


def plotRegionStats(reports, stateReport):
    pvMap.clear()
    infMap.clear()
    pprMap.clear()

    pv = c.getPercentVaccinated(reports,mul100=True)
    inf = c.getPercentageInfections(reports,mul100=True)
    hr = c.getPercentageHighRisk(reports,mul100=True)
    #R0 = c.getR0(reports)


    #hr = c.getPercentageHighRisk(reports,mul100=True)
    ppr = c.getPointsPerRegion()
    ppr = numpy.reshape(ppr, (columns,rows), order="F")
    pprMap.set_title("First-Dose Need Function")
    pprMap.axis('off')
    im3 = pprMap.imshow(ppr, cmap='OrRd', interpolation='nearest', vmin=0, vmax=1)
    texts = annotate_heatmap(im3,valfmt="{x}",threshold=0.7)

    pv = numpy.reshape(pv, (columns,rows), order="F")
    pvMap.set_title("Percent Fully Vaccinated")
    pvMap.axis('off')
    im = pvMap.imshow(pv, cmap='Blues', interpolation='nearest', vmin=0, vmax=100)
    texts = annotate_heatmap(im,threshold=70,valfmt="{x}%")

    inf = numpy.reshape(inf, (columns,rows), order="F")
    infMap.set_title("Percent Infected")
    infMap.axis('off')
    im2 = infMap.imshow(inf, cmap='OrRd', interpolation='nearest', vmin=0, vmax=100)
    texts = annotate_heatmap(im2,threshold=70,valfmt="{x}%")


    #R0 = c.getR0(reports)
    #R0= numpy.reshape(R0, (columns,rows), order="F")
    #R0Map.set_title("R0")
    #R0Map.axis('off')
    #im4 = R0Map.imshow(R0, cmap='OrRd', interpolation='nearest', vmin=0, vmax=3)
    #texts = annotate_heatmap(im4,threshold=70,valfmt="{x}%")

    surf = writeToScreen(heatCanvas)
    return(surf)

def plotPercentageInfections(reports, stateReport):
    infMap.clear()
    inf = c.getPercentageInfections(reports,mul100=True)
    inf = numpy.reshape(inf, (columns,rows), order="F")
    pvMap.set_title("Percent Infected")
    pvMap.axis('off')
    im = pvMap.imshow(inf, cmap='Blues', interpolation='nearest')
    texts = annotate_heatmap(im,threshold=70,valfmt="{x}%")
    surf = writeToScreen(heatCanvas)
    return(surf)

def addTextbox(text, loc, size="small",color=BLACK):
    f = font
    if(size == "large"):
        f = font2
    elif(size == "button"):
        f = smallfont
    text_surf = f.render(text, True, color)
    screen.blit(text_surf, loc)

buttonX = 820
buttonY = 40

go = True
notComplete = True
finalDay = -1
finalDeaths = -1

if(algorithm == "even"):
    c.setControlAlgorithm(algorithm="even")
else:
    c.setControlAlgorithm(algorithm="weighted")


#c.setControlAlgorithm(algorithm="even")
while True: 
    #if(c.algorithm == "even"):
    mouse = pygame.mouse.get_pos()

    screen.fill((255, 255, 255))
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if buttonX <= mouse[0] <= buttonX+140 and buttonY <= mouse[1] <= buttonY+40:
        pygame.draw.rect(screen,color_light,[buttonX,buttonY,140,40])
        
    else:
        pygame.draw.rect(screen,color_dark,[buttonX,buttonY,140,40])

    if(go):
        addTextbox("Pause", (buttonX+30,buttonY+5), size="button")
        notComplete = c.tick_time(verbose=False)
        s = c.state
        m = s.get_region(2,2)

        reports = c.getCurrentRegionReports()
        stateReport = c.getCurrentStateReport()
    else:
        addTextbox("Start", (buttonX+30,buttonY+5), size="button")
            
    surf = plotRegionStats(reports, stateReport)
    screen.blit(surf, (-10,300))
    R0 = c.getR0(reports)

    surf = plotStateOverview(reports, stateReport)
    screen.blit(surf, (10, 10))

    addTextbox("Simulation Day: " + str(stateReport.get_day()), (800, 10))
    addTextbox("COVID-19 Dashboard", (400, 10))

    if(notComplete):
        addTextbox("Pfizer Unused: " + str(round(stateReport.get_pfizer()/1000,2)) + "k", (755, 110))
        addTextbox("Moderna Unused: " + str(round(stateReport.get_moderna()/1000,2)) + "k", (755, 130))
        if(c.getDeaths() < 1000):
            addTextbox("Total Deaths: " + str(int(c.getDeaths())), (755, 150))   
        else:
            addTextbox("Total Deaths: " + str(round(c.getDeaths()/1000, 3)) + "k", (755, 150))  
        if(sum(c.getSusceptible(reports)) < 1):
            addTextbox("All First-Doses Delivered! ", (755, 90))
        else:
            addTextbox("Vaccinations Underway ", (755, 90))
    else:
        if((finalDay == -1) and (finalDeaths == -1)):
            finalDay = c.getDay()
            finalDeaths = c.getDeaths()
        addTextbox("All Persons Vaccinated!", (755, 90))
        addTextbox("Final Day: " + str(finalDay), (755, 110))
        addTextbox("Total Vaccinated: " + str(round(c.getTotalVaccinated(reports)/1000,3)) + "k", (755, 130))
        addTextbox("Final Deaths: " + str(round(c.getDeaths()/1000,3)) + "k", (755, 150))  
    if(c.algorithm == "even"):
        addTextbox("Even Distribution Enabled", (10, 10), color=RED)  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if the mouse is clicked on the
            # button the game is terminated
            if buttonX <= mouse[0] <= buttonX+140 and buttonY <= mouse[1] <= buttonY+40:
                go = not go

    pygame.display.update()
    clock.tick(120)