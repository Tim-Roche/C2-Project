import math
from Report import Report

class RegionModel:
    def __init__(self, name=0, N=1000, I0=1, R0=0, beta=0.2, gamma=1./10):
        self.name = name
        # Total population, N.
        self.N = N
        # Initial number of infected and recovered individuals, I0 and R0.
        self.I0, self.R0 = I0, R0
        # Everyone else, S0, is susceptible to infection initially.
        self.S0 = self.N - self.I0 - self.R0
        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        self.beta, self.gamma = beta, gamma
        self.susceptible = [self.S0]
        self.infected = [self.I0]
        self.recovered = [self.R0]
        self.vaccinated = [0]
        self.dead = [0]
        self.time = [0]
        self.units = 1
        self.dt = 1
        self.vaccine_count = 200
        self.vac_q = []
        self.death_rate = 0.018
        self.vac_flag = False

    def get_vaccine(self, vac):
        self.vaccine_count += vac
        
    def tick_time(self):
        t = self.units*self.dt
        self.time.append(t)
        d_dea = 0
        if len(self.dead) >= 14:
            d_dea = min(math.ceil(self.infected[t-14]*self.death_rate), self.infected[t-1])
        d_sus_inf = min(math.ceil((self.beta*self.susceptible[t - 1]*(self.infected[t - 1]))/self.N - self.gamma*(self.infected[t - 1])), self.susceptible[t - 1])
        d_vac_inf = min(math.ceil((self.beta * self.vaccinated[t - 1] * (self.infected[t - 1])) / self.N - self.gamma * (self.infected[t - 1])), self.vaccinated[t - 1])
        d_rec = min(math.ceil(self.gamma*(self.infected[t - 1])), self.infected[t - 1])
        d_vac = min(min(math.ceil(0.005*self.susceptible[t - 1]), self.susceptible[t - 1]), self.vaccine_count)  # Issue with d_vac_inf
        self.vaccine_count -= d_vac
        self.vac_q.append(d_vac)
        if len(self.vac_q) == 28 or self.vac_flag:
            self.vac_flag = True
            d_vac -= self.vac_q[0] + d_vac_inf
            d_rec += self.vac_q[0]
            del self.vac_q[0]
        self.infected.append(self.infected[t - 1] + d_sus_inf + d_vac_inf - d_dea)
        self.recovered.append(self.recovered[t-1] + d_rec)
        self.dead.append(self.dead[t-1] + d_dea)
        self.vaccinated.append(self.vaccinated[t-1] + d_vac)
        self.susceptible.append(self.N - self.infected[t] - self.recovered[t] - self.dead[t] - self.vaccinated[t])
        self.units += 1
        report = Report(self.name, self.N, self.infected[t], self.dead[t], self.susceptible[t], self.recovered[t], self.beta, t)
        #print(self.susceptible[t] + self.infected[t] + self.recovered[t] + self.dead[t] + self.vaccinated[t])
        print(self.vac_q)
        return report
