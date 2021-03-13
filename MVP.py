import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from RegionModel import RegionModel
 
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

dt = 1 #Day
SIMULATION_TIME = 160 #Days 
FRAMES_SECOND = 50
units = SIMULATION_TIME/dt

m = RegionModel()

def animate(i):
    m.tick_time()

    ax1.clear()
    ax1.plot(m.time, m.infected, label='Infected')
    ax1.plot(m.time, m.susceptible, label='Susceptible')
    ax1.plot(m.time, m.recovered, label='Recovered')
    ax1.plot(m.time, m.dead, label='Dead')
    ax1.plot(m.time, m.vaccinated, label='Fully Vaccinated')
    ax1.legend()
    
ani = animation.FuncAnimation(fig, animate, interval=FRAMES_SECOND)
plt.show()