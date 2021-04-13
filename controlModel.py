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

    def getPercentVaccinated(self, reports):
        allRegionVaccinations = []
        for cr in reports:
            for report in cr:
                vaccinations = report.get_vaccinated()
                population = report.get_population()
                dead = report.get_dead()
                recovered = report.get_recovered()
                allRegionVaccinations.append(vaccinations/(population - dead - recovered))
        return(allRegionVaccinations)    

    def PRR(self, values, names):
        normRank = []
        numOfRegions = len(names)
        values, names = zip(*sorted(zip(values,names), reverse=True))
        PRRlist = []
        for rank in range(1,len(values)+1):
            percentageRegionRank = 1.1-rank/numOfRegions
            PRRlist.append(percentageRegionRank)
        names, PRRlist = zip(*sorted(zip(names,PRRlist)))
        return(PRRlist)

    def getPercentageInfections(self, reports):
        allRegionInfections = []
        regionNames = []
        for cr in reports:
            for report in cr:
                infections = report.get_infected()
                susceptible = report.get_susceptible()
                population = report.get_population()
                percentInfections = 0
                if(infections+susceptible != 0):
                    percentInfections = (infections)/(population)
                allRegionInfections.append(percentInfections)
                regionNames.append(report.get_region())
        return(allRegionInfections)

    def getPRRpercentInfections(self, reports):
        allRegionInfections = self.getPercentageInfections(reports)
        regionNames = [x for x in range(0, len(allRegionInfections))]
        PRR_percentInfections = self.PRR(allRegionInfections, regionNames)
        return(PRR_percentInfections)   

    def getPercentageHighRisk(self, reports):
        rs = []
        regionNames = []
        for cr in reports:
            for report in cr:
                r = report.get_r()
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
        norm = np.linalg.norm(array)
        normal_array = list(array/norm)
        output = np.reshape(normal_array, (self.columns,self.rows), order="F")
        return(output)

    def calculateDistroPlan(self, reports):
        PRR_percentInfections = self.getPRRpercentInfections(reports)
        PRR_percentageHighRisk = self.getPRRpercentageHighRisk(reports)
        PRR_R0 = self.getPRR_R0(reports)
        pointsPerRegion = list(np.add(PRR_percentInfections, PRR_percentageHighRisk))
        pointsPerRegion = np.add(pointsPerRegion, PRR_R0)
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

    def tick_time(self, verbose=False):
        notComplete = True
        state_report, reports = self.state.tick_time()
        self.reports = reports

        pfizer_reserved_map, moderna_reserved_map, reservedPfizer, reservedModerna = self.calculateReservedVaccines(reports)
        self.state.distribute_vaccines(pfizer_reserved_map, moderna_reserved_map, maxPfizer = reservedPfizer, maxModerna = reservedModerna)
        masterDistroPlan = self.calculateDistroPlan(reports)
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
                    continue
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