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
                percentInfections = 0
                if(infections+susceptible != 0):
                    percentInfections = (infections)/(infections + susceptible)
                allRegionInfections.append(percentInfections)
                regionNames.append(report.get_region())
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
        PRR_R0 = self.PRR(R0s, regionNames)
        return(PRR_R0)

    def normalizeAndReshape(self, array):
        norm = np.linalg.norm(array)
        normal_array = list(array/norm)
        output = np.reshape(normal_array, (self.columns,self.rows), order="F")
        return(output)

    def calculateDistroPlan(self, reports):
        PRR_percentInfections = self.getPercentageInfections(reports)
        PRR_percentageHighRisk = self.getPercentageHighRisk(reports)
        PRR_R0 = self.getR0(reports)
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

    def run(self):
        run = True
        while run:
            state_report, reports = self.state.tick_time()

            pfizer_reserved_map, moderna_reserved_map, reservedPfizer, reservedModerna = self.calculateReservedVaccines(reports)
            self.state.distribute_vaccines(pfizer_reserved_map, moderna_reserved_map, maxPfizer = reservedPfizer, maxModerna = reservedModerna)
            masterDistroPlan = self.calculateDistroPlan(reports)
            self.state.distribute_vaccines(masterDistroPlan, masterDistroPlan)
        

            remaining = state_report.get_population() - (state_report.get_recovered() + state_report.get_vaccinated() + state_report.get_dead())
            if(remaining <= 0):
                run = False
                
            
            print("-----------")
            print(state_report)
            print()
            for rx in reports:
                for ry in rx:
                    continue
                    #print(ry)
            #        if ((ry.get_pfizer() - int(ry.get_pfizer())) != 0):
            #            run = False
            print(state_report.get_population() - (state_report.get_recovered() + state_report.get_vaccinated() + state_report.get_dead()))
            #time.sleep(0.1)

c = controlModel(2, 2)
c.run()
print("Done!")