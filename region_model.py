class region_model:
    def __init__(self, N=1000, I0=1, R0=0, beta=0.2, gamma=1./10):
        # Total population, N.
        self.N = 1000
        # Initial number of infected and recovered individuals, I0 and R0.
        self.I0, self.R0 = I0, R0
        # Everyone else, S0, is susceptible to infection initially.
        self.S0 = self.N - self.I0 - self.R0
        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        self.beta, self.gamma = beta, gamma
        self.susceptible = [self.S0]
        self.infected = [self.I0]
        self.recovered = [self.R0]
        self.dead = [0]
        self.time = [0]
        self.units = 1
        self.dt = 1

    def tickTime(self):
        t = self.units*self.dt
        self.time.append(t)
        d_dea = 0
        if len(self.dead) >= 14:
            d_dea = self.infected[t-14]*0.018
        d_sus = -1*(self.beta*self.susceptible[t - 1]*self.infected[t - 1])/self.N
        d_inf = (self.beta*self.susceptible[t - 1]*self.infected[t - 1])/self.N - self.gamma*self.infected[t - 1] 
        d_rec = self.gamma*self.infected[t - 1]
        
        self.susceptible.append(self.susceptible[t-1] + d_sus)
        self.infected.append(self.infected[t-1] + d_inf)
        self.recovered.append(self.recovered[t-1] + d_rec - d_dea)
        self.dead.append(self.dead[t-1] + d_dea)
        self.units += 1
        print(self.susceptible[-1] + self.infected[-1] + self.recovered[-1] + self.dead[-1])