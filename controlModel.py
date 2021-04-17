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
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.state = StateModel(self.rows,self.columns)
        self.reports = None
        self.stateReports = None
        self.pointsPerRegion = None
        self.toggle = False

    def getPercentVaccinated(self, reports, mul100=False):
        allRegionVaccinations = []
        for cr in reports:
            for report in cr:
                vaccinations = report.get_vaccinated()
                population = report.get_population()
                dead = report.get_dead()
                recovered = report.get_recovered()
                PV = vaccinations/(population - dead - recovered)
                PV = min(1, PV)
                if(mul100):
                    PV = PV*100
                    PV = int(PV)
                allRegionVaccinations.append(PV)
        return(allRegionVaccinations)    

    def scale(self, values, weight=1):
        if(sum(values) > 0):
            return([(weight*value)/sum(values) for value in values])  
        else:
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
                allRPop.append(sus)
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

    def normalizeAndReshape(self, array):
        #print(sum(array))
        #print(array)
        if(sum(array) > 0):
            #print(sum(array))
            normal_array = [element/sum(array) for element in array]
        else:
            normal_array = [0 for element in array]
        output = np.reshape(normal_array, (self.columns,self.rows), order="F")
        return(output)

    def roundList(self, l):
        return([round(i,2) for i in l])

    def calculateDistroPlan(self, reports,force=None):
        normInfRate = self.scale(self.getInfectionRate(reports),100) #self.getPRRpercentInfections(reports)
        #print(normInfRate)
        normHR = self.scale(self.getPercentageHighRisk(reports),1) #self.getPRRpercentageHighRisk(reports)
        normSus = self.scale(self.getSusceptible(reports),50) #self.getPRR_R0(reports)
        normPIN =  self.scale(self.getPercentageInfections(reports),1)
        #print(self.roundList(list(normInfRate[0:3])))
        #print(self.roundList(list(normHR[0:3])))
        #print(self.roundList(list(normSus[0:3])))
        #print()
        self.pointsPerRegion = list(np.add(normInfRate, normHR))
        self.pointsPerRegion = np.add(self.pointsPerRegion, normSus)
        self.pointsPerRegion = np.add(self.pointsPerRegion, normPIN)
        if(force != None):
            self.pointsPerRegion = force
        masterPlan = self.normalizeAndReshape(self.pointsPerRegion)
        #print(masterPlan)
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

    def getPointsPerRegion(self):
        return([round(r,2) for r in self.pointsPerRegion])

    def tick_time(self, verbose=False):
        notComplete = True
        state_report, reports = self.state.tick_time()
        self.reports = reports
        self.stateReports = state_report

        if(state_report.get_infected() < 50000):
            if(self.toggle):
                print(state_report.get_infected(), state_report.get_day())
                print("Dead: ", state_report.get_dead())
                print("Vaccinated: ", state_report.get_vaccinated())
                self.toggle = False
        else:
            self.toggle = True

        regionSizes = []
        for rx in reports:
            for ry in rx:
                regionSizes.append(int(ry.get_isSmallRegions()))
        regionSizes = np.reshape(regionSizes, (self.columns,self.rows), order="F")


        pfizer_reserved_map, moderna_reserved_map, reservedPfizer, reservedModerna = self.calculateReservedVaccines(reports)


        self.state.distribute_vaccines(pfizer_reserved_map, moderna_reserved_map, maxPfizer = reservedPfizer, maxModerna = reservedModerna)
        masterDistroPlan = self.calculateDistroPlan(reports) #,force=[0,0,0,0,0,0,0,0,0]


        smallRegionsOnly = np.multiply(masterDistroPlan, regionSizes)
        totalSmallVaccines = sum(list(np.array(smallRegionsOnly)*self.stateReports.get_available_moderna()))
        

        #totalVaccines = get_available_pfizer() + get_available_moderna()
        #absoluteDistro = [i*totalVaccines for i in masterDistroPlan]

        #print(masterDistroPlan)
        self.state.distribute_vaccines(masterDistroPlan, masterDistroPlan)
    

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
        return(notComplete)

    def getDay(self):
        return(self.state.get_day())
"""
c = controlModel(2, 2)

notComplete = True
while notComplete:
    notComplete = c.tick_time(verbose=True)
print("Done!")
"""