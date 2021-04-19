from controlModel import controlModel
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

#fig2 = plt.figure()
#bx1 = fig.add_subplot(1,1,1)
#bx1.plot([1, 2, 3], [4,5,6], label='Susceptible')
plt.show()

FRAMES_SECOND = 60
c = controlModel(columns, rows)
s = c.state

totalInfected = []
totalSusceptible = []
totalRecovered = []
totalDay = []
totalDead = []
totalVaccinated = []
totalSusHR = []
def animate(i):
    c.tick_time(verbose=True)
    s = c.state
    m = s.get_region(2,2)

    reports = c.getCurrentRegionReports()
    stateReport = c.getCurrentStateReport()

    infected = c.getPercentageInfections(reports)
    highRisk = c.getPercentageHighRisk(reports)
    vaccinated = c.getPercentVaccinated(reports)
    R0 = c.getR0(reports)

    totalInfected.append(stateReport.get_infected())
    totalDay.append(stateReport.get_day())
    totalSusceptible.append(stateReport.get_susceptible())
    totalRecovered.append(stateReport.get_recovered())
    totalDead.append(stateReport.get_dead())
    totalVaccinated.append(stateReport.get_vaccinated())
    totalSusHR.append(stateReport.get_r() * stateReport.get_susceptible())
    ax1.clear()
    ax1.plot(totalDay, totalInfected, label='Infected')
    ax1.plot(totalDay, totalSusceptible, label='Susceptible')
    ax1.plot(totalDay, totalRecovered, label='Recovered')
    ax1.plot(totalDay, totalDead, label='Dead')
    ax1.plot(totalDay, totalVaccinated, label='Fully Vaccinated')
    ax1.plot(totalDay, totalSusHR, label='High Risk Population')
    #ax1.title.set_text("Region 1")
    ax1.legend()

ani = animation.FuncAnimation(fig, animate, interval=FRAMES_SECOND)
plt.show()





