import pygame, sys
from pygame.locals import *
import numpy as np
import numpy 
import matplotlib
import matplotlib.animation as animation
from controlModel import controlModel
import Report

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

fig = plt.figure(figsize=[8, 4])
statePlot = fig.add_subplot(111)
stateCanvas = agg.FigureCanvasAgg(fig)

fig2 = plt.figure(figsize=[8, 5])
pvMap = fig2.add_subplot(1,3,1)
infMap = fig2.add_subplot(1,3,2)
hrMap = fig2.add_subplot(1,3,3)

heatCanvas = agg.FigureCanvasAgg(fig2)





def writeToScreen(canvas):
   canvas.draw()
   renderer = canvas.get_renderer()

   raw_data = renderer.tostring_rgb()
   size = canvas.get_width_height()
   
   return pygame.image.fromstring(raw_data, size, "RGB")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 1000))
font = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont(None, 50)


pygame.display.set_caption('C2 Final Project')

totalInfected = []
totalSusceptible = []
totalRecovered = []
totalDay = []
totalDead = []
totalVaccinated = []
totalSusHR = []
c = controlModel(columns, rows)
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
    hrMap.clear()

    pv = c.getPercentVaccinated(reports,mul100=True)
    
    pv = numpy.reshape(pv, (columns,rows), order="F")
    pvMap.set_title("Percent Vaccinated")
    pvMap.axis('off')
    im = pvMap.imshow(pv, cmap='Blues', interpolation='nearest', vmin=0, vmax=100)
    texts = annotate_heatmap(im,threshold=70,valfmt="{x}%")


    inf = c.getPercentageInfections(reports,mul100=True)
    inf = numpy.reshape(inf, (columns,rows), order="F")
    infMap.set_title("Percent Infected")
    infMap.axis('off')
    im2 = infMap.imshow(inf, cmap='OrRd', interpolation='nearest', vmin=0, vmax=100)
    texts = annotate_heatmap(im2,threshold=70,valfmt="{x}%")

    hr = c.getPercentageHighRisk(reports,mul100=True)
    hr = numpy.reshape(hr, (columns,rows), order="F")
    hrMap.set_title("Percent High Risk")
    hrMap.axis('off')
    im3 = hrMap.imshow(inf, cmap='OrRd', interpolation='nearest', vmin=0, vmax=100)
    texts = annotate_heatmap(im3,threshold=70,valfmt="{x}%")


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

def addTextbox(text, loc, size="small"):
    f = font
    if(size == "large"):
        f = font2
    text_surf = f.render(text, True, BLACK)
    screen.blit(text_surf, loc)

while True: 
    screen.fill((255, 255, 255))
    c.tick_time()
    s = c.state
    m = s.get_region(2,2)

    reports = c.getCurrentRegionReports()
    stateReport = c.getCurrentStateReport()
    

    surf = plotRegionStats(reports, stateReport)
    screen.blit(surf, (10,300))
    R0 = c.getR0(reports)

    surf = plotStateOverview(reports, stateReport)
    screen.blit(surf, (10, 10))


    addTextbox("Simulation Day: " + str(stateReport.get_day()), (800, 10))
    addTextbox("COVID-19 Dashboard", (400, 10))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(30)