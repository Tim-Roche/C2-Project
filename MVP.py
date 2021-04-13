import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from RegionModel import RegionModel
from StateModel import StateModel

ROWS = 2
COLUMNS = 2

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

FRAMES_SECOND = 60

s = StateModel(ROWS,COLUMNS)
count = 0

def animate(i):
    s.tick_time()
    day = s.get_day()
    s.distribute_vaccines([[0.25,0.25],[0.25,0.25]], [[0.25,0.25],[0.25,0.25]])
    if(day%4 == 0): 
        m = s.get_region(0,0)
        ax1.clear()
        ax1.plot(m.time, m.infected, label='Infected')
        ax1.plot(m.time, m.susceptible, label='Susceptible')
        ax1.plot(m.time, m.recovered, label='Recovered')
        ax1.plot(m.time, m.dead, label='Dead')
        ax1.plot(m.time, m.vaccinated, label='Fully Vaccinated')
        ax1.plot(m.time, m.susHR, label='High Risk Population')
        ax1.title.set_text("Region 1")
        ax1.legend()

    if(day%4 == 1): 
        m = s.get_region(0,1)

        ax2.clear()
        ax2.plot(m.time, m.infected, label='Infected')
        ax2.plot(m.time, m.susceptible, label='Susceptible')
        ax2.plot(m.time, m.recovered, label='Recovered')
        ax2.plot(m.time, m.dead, label='Dead')
        ax2.plot(m.time, m.vaccinated, label='Fully Vaccinated')
        ax2.plot(m.time, m.susHR, label='High Risk Population')
        ax2.title.set_text("Region 2")
        ax2.legend()

    if(day%4 == 2):
        m = s.get_region(1,0)

        ax3.clear()
        ax3.plot(m.time, m.infected, label='Infected')
        ax3.plot(m.time, m.susceptible, label='Susceptible')
        ax3.plot(m.time, m.recovered, label='Recovered')
        ax3.plot(m.time, m.dead, label='Dead')
        ax3.plot(m.time, m.vaccinated, label='Fully Vaccinated')
        ax3.plot(m.time, m.susHR, label='High Risk Population')
        ax3.title.set_text("Region 3")
        ax3.legend()

    if(day%4 == 3):
        m = s.get_region(1,1)

        ax4.clear()
        ax4.plot(m.time, m.infected, label='Infected')
        ax4.plot(m.time, m.susceptible, label='Susceptible')
        ax4.plot(m.time, m.recovered, label='Recovered')
        ax4.plot(m.time, m.dead, label='Dead')
        ax4.plot(m.time, m.vaccinated, label='Fully Vaccinated')
        ax4.plot(m.time, m.susHR, label='High Risk Population')
        ax4.title.set_text("Region 4")
        ax4.legend()

    #ax2.clear()
    #ax2.plot(m.time, m.susHR, label='High Risk Population')
    #ax2.legend()

ani = animation.FuncAnimation(fig, animate, interval=FRAMES_SECOND)
plt.show()