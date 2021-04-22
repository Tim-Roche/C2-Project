import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from RegionModel import RegionModel
from StateModel import StateModel
from Report import Report
import time

class controlModel():
    def __init__(self, rows, columns, weights):
        self.rows = rows
        self.columns = columns
        self.state = StateModel(self.rows,self.columns)
        self.reports = None
        self.stateReports = None
        self.undistributedPfizer = 0
        self.undistributedModerna = 0
        self.pointsPerRegion = [0 for i in range (0, rows*columns)]
        self.toggle = False
        self.weights = weights
        self.ratePrev = None


    def getPercentVaccinated(self, reports, mul100=False, inverse=False):
        allRegionVaccinations = []
        for cr in reports:
            for report in cr:
                vaccinations = report.get_vaccinated()
                population = report.get_population()
                dead = report.get_dead()
                recovered = report.get_recovered()
                PV = vaccinations/(population - dead - recovered)
                #if(int(report.get_region()) == 1):
                 #   print("!!!!!")
                  #  print(vaccinations, population, dead, recovered, PV)
                PV = min(1, PV)
                if(mul100):
                    PV = PV*100
                    PV = int(PV)
                if(inverse):
                    PV = 1-PV
                allRegionVaccinations.append(PV)
        print(allRegionVaccinations)
        return(allRegionVaccinations)    

    def scale(self, values, weight):
        if(sum(values) > 0):
            return([(weight*value)/sum(values) for value in values])  
        else:
            #print(values)
            return([0 for value in values])

    def PRR(self, values, weight=1):
        normRank = []
        names = [i for i in range(0, len(values))]
        numOfRegions = len(names)
        values, names = zip(*sorted(zip(values,names), reverse=True))
        PRRlist = []
        for rank in range(1,len(values)+1):
            percentageRegionRank = 1-rank/numOfRegions
            PRRlist.append(weight*percentageRegionRank)
        names, PRRlist = zip(*sorted(zip(names,PRRlist)))
        return(PRRlist)

    def getPercentageInfections(self, reports, mul100=False):
        allRegionInfections = []
        regionNames = []
        for cr in reports:
            for report in cr:
                infections = report.get_infected()
                susceptible = report.get_susceptible()
                population = report.get_population()
                dead = report.get_dead()
                vaccinated = report.get_vaccinated()
                recovered = report.get_recovered()
                percentInfections = 0
                total = population - dead - vaccinated - recovered
                if(round(total) > 0):
                    percentInfections = (round(infections))/(round(total))
                else:
                    percentInfections = 0
                if(mul100 == True):
                    percentInfections = int(percentInfections*100)
                    
                allRegionInfections.append(percentInfections)
                regionNames.append(report.get_region())
        return(allRegionInfections)

    def getPRRpercentInfections(self, reports):
        allRegionInfections = self.getPercentageInfections(reports)
        regionNames = [x for x in range(0, len(allRegionInfections))]
        PRR_percentInfections = self.PRR(allRegionInfections, regionNames)
        return(PRR_percentInfections)   

    def getInfectionRate(self,reports):
        allInfectionRates = []
        for cr in reports:
            for report in cr:
                irate = report.get_d_inf()
                irate = max(irate,0)
                allInfectionRates.append(irate)
        return(allInfectionRates)       

    def getInfectionRateRate(self,reports):
        allInfectionRates = self.getInfectionRate(reports)
        if(self.ratePrev == None):
            self.ratePrev = allInfectionRates
        IRR = np.subtract(allInfectionRates, self.ratePrev)
        self.ratePrev = allInfectionRates
        return(IRR)

    def getPercentageHighRisk(self, reports, mul100=False):
        rs = []
        regionNames = []
        for cr in reports:
            for report in cr:
                r = report.get_r()
                if(mul100==True):
                    r = int(r*100)
                rs.append(r)
                regionNames.append(report.get_region())
        return(rs)
    
    def getSusceptible(self, reports):
        allRPop = []
        for cr in reports:
            for report in cr:
                sus = report.get_susceptible()
                allRPop.append(max(sus,0))
        return(allRPop)      

    def getPRRpercentageHighRisk(self, reports):
        rs = self.getPercentageHighRisk(reports)
        regionNames = [x for x in range(0, len(rs))]
        PRR_percentageHighRisk = self.PRR(rs, regionNames)
        return(PRR_percentageHighRisk)

    def getR0(self, reports):
        R0s = []
        regionNames = []
        for cr in reports:
            for report in cr:
                gamma = report.get_gamma()
                beta = report.get_beta()
                R0 = beta/gamma
                R0s.append(R0)
                regionNames.append(report.get_region())
        return(R0s)

    def getPRR_R0(self, reports):
        R0s = self.getR0(reports)
        regionNames = [x for x in range(0, len(R0s))]
        PRR_R0 = self.PRR(R0s, regionNames)
        return(PRR_R0)

    def getVaccineLimit(self, reports, cost=False):
        limits = []
        for cr in reports:
            for report in cr:
                numVac = report.get_pfizer() + report.get_moderna()
                max_n = report.get_distroLimit()
                limit = max_n - numVac
                if cost:
                    limit = min(numVac/max_n,1)
                    limit = 1 - limit
                #limit = max(limit,0.0)
                limits.append(limit)
        return(limits)

    def getPPRVaccineLimit(self, reports):
        limits = self.getVaccineLimit(reports)
        regionNames = [x for x in range(0, len(limits))]
        PRR_limit = self.PRR(limits, regionNames)
        return(PRR_limit)


    def normalizeAndReshape(self, array):
        output = array
        array = np.reshape(array, (self.columns*self.rows), order="F")
        total = sum(array)
        if total != 0:
            normal_array = [element/total for element in array]
            output = np.reshape(normal_array, (self.columns,self.rows), order="F")
        return(output)

        #print(sum(array))
        #print(array)
        #if(sum(array) > 0):
            #print(sum(array))
            #normal_array = [element/sum(array) for element in array]
        #else:
        #    normal_array = [0 for element in array]
        #output = np.reshape(normal_array, (self.columns,self.rows), order="F")
        #return(output)

    def roundList(self, l):
        return([round(i,2) for i in l])

    def calculateDistroPlan(self, reports,force=None):
        normInfRate = self.scale(self.getInfectionRate(reports),self.weights[0]) #self.getPRRpercentInfections(reports)
        #print(normInfRate)
        normHR = self.scale(self.getPercentageHighRisk(reports),self.weights[1]) #self.getPRRpercentageHighRisk(reports)
        normSus = self.scale(self.getPercentVaccinated(reports, inverse=True),self.weights[2]) #self.getPRR_R0(reports)
        #normPIN =  self.scale(self.getPercentageInfections(reports),self.weights[3])
        #lim =  self.scale(self.getVaccineLimit(reports),self.weights[3])
        normPV = self.scale(self.getInfectionRateRate(reports), self.weights[3])
        #print(self.roundList(list(normInfRate[0:3])))
        #print(self.roundList(list(normHR[0:3])))
        #print(self.roundList(list(normSus[0:3])))
        #print()
        self.pointsPerRegion = list(np.add(normInfRate, normHR))
        self.pointsPerRegion = np.add(self.pointsPerRegion, normSus)
        self.pointsPerRegion = np.add(self.pointsPerRegion, normPV)
        #print(self.getVaccineLimit(reports))
        #overflowMask = [int(x >= 0) for x in self.getVaccineLimit(reports)]
        #self.pointsPerRegion = np.multiply(self.pointsPerRegion, overflowMask)
        if(force != None):
            self.pointsPerRegion = force
        masterPlan = self.normalizeAndReshape(self.pointsPerRegion)
        return masterPlan

    def calculateReservedVaccines(self, reports):
        pfizer_reserved_map = []
        moderna_reserved_map = []
        for cr in reports:
            for report in cr:   
                pfizer_reserved = report.get_rollingSevenDays_P()
                moderna_reserved = report.get_rollingSevenDays_M()
                pfizer_reserved_map.append(pfizer_reserved)
                moderna_reserved_map.append(moderna_reserved)

        reservedPfizer = sum(pfizer_reserved_map)
        reservedModerna = sum(moderna_reserved_map)
        if(reservedPfizer != 0):   
            pfizer_reserved_map = self.normalizeAndReshape(pfizer_reserved_map)
        else:
            pfizer_reserved_map = np.reshape(pfizer_reserved_map, (self.columns,self.rows), order="F")
        if(reservedModerna != 0):
            moderna_reserved_map = self.normalizeAndReshape(moderna_reserved_map)
        else:
            moderna_reserved_map = np.reshape(moderna_reserved_map, (self.columns,self.rows), order="F")

        return(pfizer_reserved_map, moderna_reserved_map, reservedPfizer, reservedModerna)

    def getCurrentRegionReports(self):
        return(self.reports)

    def getCurrentStateReport(self):
        return(self.stateReports)

    def distributeReservedVaccines(self):
        pfizer_reserved_map, moderna_reserved_map, reservedPfizer, reservedModerna = self.calculateReservedVaccines(self.reports)
        print(pfizer_reserved_map)
        self.state.distribute_vaccines(pfizer_reserved_map, moderna_reserved_map, maxPfizer=reservedPfizer,maxModerna=reservedModerna)
        self.undistributedPfizer -= reservedPfizer
        self.undistributedModerna -= reservedModerna

    def distributePfizerVaccines(self, regionTotals):
        regionSizes = []
        for rx in self.reports:
            for ry in rx:
                regionSizes.append(int(not ry.get_isSmallRegions()))
        mask = np.reshape(regionSizes, (self.columns, self.rows), order="F")
        regionTotals = np.reshape(regionTotals, (self.columns, self.rows), order="F")
        try:
            pfizerOnly = np.multiply(regionTotals,mask)
        except:
            #print(regionTotals)
            #print(mask)
            exit(1)
        pfizerOnly = self.normalizeAndReshape(pfizerOnly)
        self.state.distribute_vaccines(pfizerOnly, pfizerOnly, maxModerna=0)
        regionTotals= np.subtract(regionTotals, np.multiply(pfizerOnly,self.undistributedPfizer))
        self.undistributedPfizer = 0
        for row in range(0,self.rows):
            for col in range(0,self.columns):
                if regionTotals[row][col] < 0:
                    regionTotals[row][col] = 0
        return regionTotals

    def getPointsPerRegion(self):
        return([round(r,2) for r in self.pointsPerRegion])

    def tick_time(self, verbose=False):
        notComplete = True
        state_report, reports = self.state.tick_time()
        self.reports = reports
        self.stateReports = state_report

        if(state_report.get_infected() < 10):
            if(self.toggle):
                print(state_report.get_infected(), state_report.get_day())
                print("Dead: ", state_report.get_dead())
                print("Vaccinated: ", state_report.get_vaccinated())
                self.toggle = False
        else:
            self.toggle = True

    def distributeModernaVaccines(self, regionTotal):
        modernaOnly = self.normalizeAndReshape(regionTotal)
        self.state.distribute_vaccines(modernaOnly, modernaOnly)
        self.undistributedModerna = 0

    def distributeAllVaccines(self):
        # Distribute Resereved Vaccines
        self.distributeReservedVaccines()
        # Calculate Region Vaccine Percentages
        regionVaccinePerc = self.calculateDistroPlan(self.reports)
        # Calculate Region Vaccine Total
        regionVaccineTotal = list(np.multiply(regionVaccinePerc,(self.undistributedModerna + self.undistributedPfizer)))
        # Distribute Pfizer Vaccines
        regionVaccineTotal = self.distributePfizerVaccines(regionVaccineTotal)
        # Distribute Moderna Vaccines
        self.distributeModernaVaccines(regionVaccineTotal)
        # Distribute Reserved Vaccines
        self.distributeReservedVaccines()
        # Distribute All Phizer Vaccines


    def tick_time(self, verbose=False):
        notComplete = True
        state_report, reports = self.state.tick_time()
        self.reports = reports
        self.stateReports = state_report
        self.undistributedPfizer = self.stateReports.get_available_pfizer()
        self.undistributedModerna = self.stateReports.get_available_moderna()

        if self.undistributedModerna != 0 or self.undistributedPfizer != 0:
            self.distributeAllVaccines()
        remaining = state_report.get_population() - (state_report.get_recovered() + state_report.get_vaccinated() + state_report.get_dead())
        if(remaining <= 0):
            notComplete = False
        
        if verbose:
            print("-----------")
            print(state_report)
            print()
            for rx in reports:
                for ry in rx:
                    print(ry)
            print("Remaining: " + str(state_report.get_population() - (state_report.get_recovered() + state_report.get_vaccinated() + state_report.get_dead())))
            print("Recovered: " + str(state_report.get_recovered()))
            print("Vaccinated: " + str(state_report.get_vaccinated()))
            print("Dead: " + str(state_report.get_dead()))

        return(notComplete)

    def getDeaths(self):
        return self.stateReports.get_dead()

    def getDay(self):
        return(self.state.get_day())

"""
failed = False
best_weights = []
best_deaths = -1
for infectionRate in range (1,20,1):
    print(infectionRate)
    for highrisk in range (0,2,1):
        for sus in range(0, 2, 1):
            for pin in range(0, 2, 1):
                failed = False
                weights = [infectionRate,highrisk,sus,pin]
                c = controlModel(3, 3,weights)
                notComplete = True
                while notComplete:
                    notComplete = c.tick_time(verbose=False)
                    day = c.getDay()
                    if(day > 1000):
                        notComplete = False
                        failed = True
                        #print("FAILED")
                if(failed == False):
                    print("not failed " + str(c.getDeaths()))
                #print("---------------")
                #print(weights)
            #print(c.getDeaths())
                if (failed == False) and (c.getDeaths() <= best_deaths or best_deaths == -1):
                    best_deaths = c.getDeaths()
                    print(day)
                    best_weights = weights
                    print("---------------")
                    print(weights)
                    print(c.getDeaths())
"""
"""
weights = [17,1,1,1]
c = controlModel(3, 3,weights)
notComplete = True
while notComplete:
    notComplete = c.tick_time()
    #print(c.getPercentVaccinated(c.reports,mul100=True))

print(c.getDeaths())
"""