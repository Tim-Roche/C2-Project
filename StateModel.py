from RegionModel import RegionModel
from Report import Report
import random


class StateModel:
    def __init__(self, N, M):
        self._rows = N
        self._columns = M
        self._regions = []
        self._pfizer = 0
        self._moderna = 0
        self._init_regions()
        self._day = -1

    def _init_regions(self):
        region_num = 0
        area = self._rows*self._columns
        smallRegions = int(area*0.2)
        isSmallRegions = [int(i<smallRegions) for i in range(0,area)]
        random.seed(10)

        for row in range(0, self._rows):
            row_array = []
            for col in range(0, self._columns):
                index = col*self._rows + row
                regionSize = 1
                #beta = random.randint(10,25)/100
                #HRR = random.randint(10,60)/100
                HRR = random.randint(5,30)/100
                if(isSmallRegions[index]):
                    #regionSize = 250000
                    regionSize = random.randint(1,3)*100000
                    row_array.append(RegionModel(name=region_num, N=regionSize, beta=0.2,HRR=HRR, isSmallRegion=True)) #random.randint(500, 5000))
                else:    
                    #regionSize = 600000
                    regionSize = random.randint(5,7)*100000
                    row_array.append(RegionModel(name=region_num, HRR=HRR,N=regionSize)) #random.randint(500, 5000))
                    
                region_num += 1
            self._regions.append(row_array)

    def get_region(self,x,y):
        return self._regions[x][y]

    def get_all_regions(self):
        return(self._regions)

    def tick_time(self):
        reports = []
        for row in range(0, self._rows):
            row_reports = []
            for col in range(0, self._columns):
                row_reports.append(self._regions[row][col].tick_time())
            reports.append(row_reports)
        state_report = self.get_state_report(reports)
        self._day = state_report.get_day()
        if state_report.get_day() % 7 == 0:
            self._get_vaccines(state_report.get_day())

        state_report.set_available_pfizer(self._pfizer)
        state_report.set_available_moderna(self._moderna)

        return state_report, reports

    def get_day(self):
        return(self._day)

    def get_state_report(self, reports):
        state_report = None
        for i in range(0, self._rows):
            for j in range(0, self._columns):
                if state_report is None:
                    state_report = reports[i][j]
                else:
                    state_report = state_report + reports[i][j]
        return state_report

    def _get_vaccines(self, day):
        self._pfizer += int((day/7)*500)
        self._moderna += int((day/7)*500)

    def distribute_vaccines(self, pfizer_plan, moderna_plan, maxPfizer = -1, maxModerna = -1):
        if(maxPfizer == -1):
            maxPfizer = self._pfizer
        if(maxModerna == -1):
            maxModerna = self._moderna

        prev_pfizer = min(maxPfizer, self._pfizer)
        prev_moderna = min(maxModerna, self._moderna)
        for row in range(0, self._rows):
            for col in range(0, self._columns):
                d_pfizer = min(round(pfizer_plan[row][col]*prev_pfizer), self._pfizer)
                d_moderna = min(round(moderna_plan[row][col]*prev_moderna), self._moderna)
                self._regions[row][col].vaccine_pfizer_count += d_pfizer
                self._regions[row][col].vaccine_moderna_count += d_moderna
                self._pfizer -= d_pfizer
                self._moderna -= d_moderna




#state = StateModel(10,10)
#for i in range(0, 60):
#    print("---- Time: " + str(i) + " ----")
#    sr, rr = state.tick_time()
#    print("State Report")
#    print(sr)