import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
 
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

dt = 1 #Day
SIMULATION_TIME = 160 #Days 
units = SIMULATION_TIME/dt

class model:
    def __init__(self):
        # Total population, N.
        self.N = 1000
        # Initial number of infected and recovered individuals, I0 and R0.
        self.I0, self.R0 = 1, 0
        # Everyone else, S0, is susceptible to infection initially.
        self.S0 = self.N - self.I0 - self.R0
        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        self.beta, self.gamma = 0.2, 1./10 

        self.susceptible = [self.S0]
        self.infected = [self.I0]
        self.recovered = [self.R0]
        self.time = [0]
        self.units = 1
        self.dt = 1

    def tickTime(self):
        t = self.units*self.dt
        self.time.append(t)
        d_sus = -1*(self.beta*self.susceptible[t - 1]*self.infected[t - 1])/self.N
        d_inf = (self.beta*self.susceptible[t - 1]*self.infected[t - 1])/self.N - self.gamma*self.infected[t - 1] 
        d_rec = self.gamma*self.infected[t - 1]
        self.susceptible.append(self.susceptible[t-1] + d_sus)
        self.infected.append(self.infected[t-1] + d_inf)
        self.recovered.append(self.recovered[t-1] + d_rec)
        self.units += 1
m = model()

def animate(i):
    m.tickTime()

    ax1.clear()
    ax1.plot(m.time, m.infected, label='Infected')
    ax1.plot(m.time, m.susceptible, label='Susceptible')
    ax1.plot(m.time, m.recovered, label='Recovered')
    ax1.legend()
    
ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()
