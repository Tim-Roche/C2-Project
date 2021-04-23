import math
import numpy as np
from Report import Report
from vaccine import vaccine
import math
import random

class RegionModel:
    def __init__(self, isSmallRegion=False, name=0, seed = 123456, noise=False, N=1000, HRR=0.25, I0=1, R0=0, beta=0.2, gamma=1./20,startDate=0):
        self.name = name
        # Total population, N.
        self.N = N
        self.susHR = [self.N*HRR]
        self.startDate = startDate
        # Initial number of infected and recovered individuals, I0 and R0.
        self.I0, self.R0 = I0, R0
        # Everyone else, S0, is susceptible to infection initially.
        self.S0 = self.N - self.I0 - self.R0
        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        self.seed = seed + name
        self.beta,  self.gamma = beta, gamma
        self.susceptible = [self.S0]
        self.susceptibleNoVax = [self.S0]
        self.infected = [self.I0]
        self.ratio = [HRR]
        self.recovered = [self.R0]
        self.vaccinated = [0]
        self.dead = [0]
        self.noise = noise
        self.time = [0]
        self.units = 1
        self.dt = 1
        self.hasStarted = False
        self.vaccine_pfizer_count = 0 #Phizers recieved on a weekly basis
        self.vaccine_moderna_count = 0 #Modernas recieved on a weekly basis
        self.vaccine_distro_limit = N*0.05 #Vaccines can be distro-ed in a week; Per Week
        self.max_d_vac = round(self.vaccine_distro_limit/7) #min(self.vaccine_count, self.vaccine_limit)/7 
        self.death_rate = {"normal": 0.018, "high":0.05}
        self.vac_q = []
        self.isSmallRegion = isSmallRegion
        self.totalSingleVac = 0

        pfizer = vaccine("pfizer")
        moderna = vaccine("moderna")
        self.vacTypes = {"pfizer": pfizer, "moderna":moderna}


    def addVaccPfizer(self, count):
        self.vaccine_pfizer_count += count
        #if(self.name == 1):
        #    print("New Pfizer!", count)
        #if(count==8024):
        #    print(self.name, "recieved the vaccc")

    def addVaccModerna(self, count):
        self.vaccine_moderna_count += count



    def tick_time(self):
        np.random.seed(self.seed*2 + self.units)

        t = self.units*self.dt
        self.time.append(t)

        if(t >= self.startDate):
            self.hasStarted = True
        #else:
            #print(self.name, t, self.startDate)

        self.vacTypes['pfizer'].addVaccines(self.vaccine_pfizer_count)
        self.vacTypes['moderna'].addVaccines(self.vaccine_moderna_count)
        self.vaccine_moderna_count = 0
        self.vaccine_pfizer_count = 0

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
                #if(self.name == 1):
                #    print("Q is long enough!")
                #    print("FOL", FOL)
                #    print("RV", v.remainingVaccines(), vacDailyLimit)
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
            #if(self.name == 2):
            #    print(highRiskDead, normRiskDead)
        d_sus = -1*(self.beta*self.susceptible[t - 1]*self.infected[t - 1])/self.N

        #d_sus = min(d_sus,0)
        d_inf = -1*(d_sus) - self.gamma*self.infected[t - 1]
        d_rec = self.gamma*self.infected[t - 1]

        if True: #self.noise:
            
            mu, sigma = 0, math.sqrt(self.gamma*self.infected[t - 1]*2) # mean and standard deviation
            noise = np.random.normal(mu, sigma)
            #print(noise)
            if(max(self.susceptible[t-1] + d_sus - d_vacA,0) - d_inf > 0):
                d_inf = d_inf + noise
                d_sus = d_sus - noise

        if(self.hasStarted):
            self.vaccinated.append(self.vaccinated[t - 1] + d_vacB)
            self.susceptible.append(max(self.susceptible[t-1] + d_sus - d_vacA,0))
            self.infected.append(max(min(self.infected[t-1] + d_inf - d_dea, self.N),0))
            self.recovered.append(max(self.recovered[t-1] + d_rec,0))
            self.dead.append(max(self.dead[t-1] + d_dea,0))
        else:
            self.vaccinated.append(self.vaccinated[t - 1])
            self.susceptible.append(self.susceptible[t-1])
            self.infected.append(self.infected[t-1])
            self.recovered.append(self.recovered[t-1])
            self.dead.append(self.dead[t-1])   
        
        self.susHR.append(max(self.susHR[t - 1] + (d_sus-d_vacA)*self.ratio[t-1], 0))
        r = 0
        if(self.susceptible[t] > 0):
            r = self.susHR[t]/self.susceptible[t]
        self.ratio.append(r)

        self.units += 1

        rolling7_P = self.vacTypes['pfizer'].rollingSevenDaySum()
        rolling7_M = self.vacTypes['moderna'].rollingSevenDaySum()

        inQ = sum(self.vacTypes['pfizer'].vac_q) + sum(self.vacTypes['moderna'].vac_q)
        s = self.susceptible[t] + self.infected[t] + inQ + self.vaccinated[t] + self.recovered[t] + self.dead[t]
        #if(self.name == 1):
            #print("Remaining Vaccs" + str(v.remainingVaccines()))
            #print("Q: ",inQ,rolling7_P,rolling7_M)
            #print(self.vacTypes['pfizer'].vac_q)
            #print(self.vacTypes['moderna'].vac_q)

        #    print("SUM: " + str(s), self.susHR[t])
        #    print(self.susceptible[t], self.infected[t],inQ,self.vaccinated[t], self.recovered[t], self.dead[t])

        report = Report(self.name, self.N, round(self.infected[t]), round(self.dead[t]), round(self.susceptible[t]), round(self.recovered[t]), round(self.vaccinated[t]),
                        self.vacTypes['pfizer'].vaccineCount, self.vacTypes['moderna'].vaccineCount, self.beta, r, self.gamma, math.ceil(rolling7_P), math.ceil(rolling7_M), self.isSmallRegion, self.vaccine_distro_limit, d_inf, t)

        return report   