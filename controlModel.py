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
            print(sum(values))
            return([(weight*value)/sum(values) for value in values])  
        else:
            return([0 for value in values])

    def PRR(self, values, names):
        normRank = []
        numOfRegions = len(names)
        values, names = zip(*sorted(zip(values,names), reverse=True))
        PRRlist = []
        for rank in range(1,len(values)+1):
            percentageRegionRank = 1-rank/numOfRegions
            PRRlist.append(percentageRegionRank)
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
        print(array)
        if(sum(array) > 0):
            normal_array = [element/sum(array) for element in array]
        else:
            normal_array = [0 for element in array]
        output = np.reshape(normal_array, (self.columns,self.rows), order="F")
        return(output)

    def roundList(self, l):
        return([round(i,2) for i in l])

    def calculateDistroPlan(self, reports):
        PRR_percentInfections = self.scale(self.getPercentageInfections(reports)) #self.getPRRpercentInfections(reports)
        PRR_percentageHighRisk = self.scale(self.getPercentageHighRisk(reports)) #self.getPRRpercentageHighRisk(reports)
        PRR_R0 = self.scale(self.getR0(reports)) #self.getPRR_R0(reports)
        print(self.roundList(list(PRR_percentInfections[0:3])))
        print(self.roundList(list(PRR_percentageHighRisk[0:3])))
        print(self.roundList(list(PRR_R0[0:3])))
        print()
        pointsPerRegion = list(np.add(PRR_percentInfections, PRR_percentageHighRisk))
        self.pointsPerRegion = np.add(pointsPerRegion, PRR_R0)
        masterPlan = self.normalizeAndReshape(pointsPerRegion)
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

        regionSizes = []
        for rx in reports:
            for ry in rx:
                regionSizes.append(int(ry.get_isSmallRegions()))
        regionSizes = np.reshape(regionSizes, (self.columns,self.rows), order="F")


        pfizer_reserved_map, moderna_reserved_map, reservedPfizer, reservedModerna = self.calculateReservedVaccines(reports)


        self.state.distribute_vaccines(pfizer_reserved_map, moderna_reserved_map, maxPfizer = reservedPfizer, maxModerna = reservedModerna)
        masterDistroPlan = self.calculateDistroPlan(reports)


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