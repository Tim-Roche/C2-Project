import math
import numpy as np
from Report import Report
from vaccine import vaccine

class RegionModel:
    def __init__(self, name=0, N=1000, HRR=0.25, I0=1, R0=0, beta=0.2, gamma=1./10):
        self.name = name
        # Total population, N.
        self.N = N
        self.susHR = [self.N*HRR]
        # Initial number of infected and recovered individuals, I0 and R0.
        self.I0, self.R0 = I0, R0
        # Everyone else, S0, is susceptible to infection initially.
        self.S0 = self.N - self.I0 - self.R0
        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        self.beta, self.gamma = beta, gamma
        self.susceptible = [self.S0]
        self.infected = [self.I0]
        self.ratio = [HRR]
        self.recovered = [self.R0]
        self.vaccinated = [0]
        self.dead = [0]
        self.time = [0]
        self.units = 1
        self.dt = 1
        self.vaccine_pfizer_count = 5 #Phizers recieved on a weekly basis
        self.vaccine_moderna_count = 5 #Modernas recieved on a weekly basis
        self.vaccine_distro_limit = 10 #Vaccines can be distro-ed in a week; Per Week
        self.max_d_vac = self.vaccine_distro_limit/7 #min(self.vaccine_count, self.vaccine_limit)/7 
        self.death_rate = {"normal": 0.018, "high":0.05}
        self.vac_q = []

        pfizer = vaccine("pfizer")
        moderna = vaccine("moderna")
        self.vacTypes = {"pfizer": pfizer, "moderna":moderna}
        
    def tick_time(self):
        t = self.units*self.dt
        self.time.append(t)
        self.vacTypes['pfizer'].addVaccines(self.vaccine_pfizer_count/7)
        self.vacTypes['moderna'].addVaccines(self.vaccine_moderna_count/7)

        #DOSE B - 2nd dose gets priority 

        vacDailyLimit = self.max_d_vac
        d_vacB = 0
        #if(len(self.vac_q) >= 28):
        for vName in self.vacTypes:
            v = self.vacTypes[vName]
            if v.queueLength() >= 28:
                #d_vacB = min(float(self.vac_q[:1][0]), self.max_d_vac)
                FOL = v.frontOfLine()
                vmax = 0
                if((v.remainingVaccines() > 0) and (vacDailyLimit > 0)):
                    vmax = min(FOL, min(v.remainingVaccines(),vacDailyLimit))
                    vmax = max(vmax, 0)
                v.vaccinate(vmax)
                vacDailyLimit -= vmax
                d_vacB += vmax 
                remaining = max(0, FOL - vmax) #We couldnt vaccinate everyone :(
                v.pop(remaining) #Puts these people at the front of the line

        d_vacA = 0
        #DOSE A
        eligibleForVaccineToday = min(self.susceptible[t - 1], vacDailyLimit)
        for vName in self.vacTypes:
            v = self.vacTypes[vName]
            vmax = 0
            if((v.remainingVaccines() > 0) and (vacDailyLimit > 0)):
                vmax = min(eligibleForVaccineToday, min(v.remainingVaccines(),vacDailyLimit))
                vmax = max(vmax, 0)
            v.vaccinate(vmax)
            v.addToQueue(vmax)
            vacDailyLimit -= vmax
            d_vacA += vmax

        #Daily Changes
        d_dead_highRisk = 0
        d_dea = 0
        if len(self.dead) >= 14:
            #High Risk
            highRiskDead = self.infected[t-14]*self.ratio[t-14]
            d_dead_highRisk = min(highRiskDead*self.death_rate['high'], self.infected[t-1]*self.ratio[t-1])

            d_dea += d_dead_highRisk

            #Normal Risk
            normRiskDead = self.infected[t-14]*(1-self.ratio[t-14])
            d_dea += min(normRiskDead*self.death_rate['normal'], self.infected[t-1]*(1-self.ratio[t-1]))

        d_sus = -1*(self.beta*self.susceptible[t - 1]*self.infected[t - 1])/self.N
        d_sus = min(d_sus - d_vacA,0)
        d_inf = -1*d_sus - self.gamma*self.infected[t - 1]
        d_rec = self.gamma*self.infected[t - 1]

        self.vaccinated.append(self.vaccinated[t - 1] + d_vacB)
        self.susceptible.append(self.susceptible[t-1] + d_sus - d_vacA)
        self.infected.append(self.infected[t-1] + d_inf - d_dea)
        self.recovered.append(self.recovered[t-1] + d_rec)
        self.dead.append(self.dead[t-1] + d_dea)
        
        self.susHR.append(max(self.susHR[t - 1] - d_vacA - d_dead_highRisk, 0))
        r = self.susHR[t]/self.susceptible[t]
        self.ratio.append(r)

        self.units += 1

        populationCheck = self.susceptible[-1] + self.infected[-1] + self.recovered[-1] + self.dead[-1] + self.vaccinated[-1] + sum(self.vacTypes['pfizer'].vac_q) + sum(self.vacTypes['moderna'].vac_q)
        #print(round(populationCheck))
        report = Report(self.name, self.N, self.infected[t], self.dead[t], self.susceptible[t], self.recovered[t], self.beta, t)
        return report