from RegionModel import RegionModel
from Report import Report
import random
​
class StateModel:
​
    def __init__(self, N, M):
        self.rows = N
        self.columns = M
        self.regions = []
        self.init_regions()
​
    def init_regions(self):
        region_num = 0
        for i in range(0, self.rows):
            row_array = []
            for j in range(0, self.columns):
                row_array.append(RegionModel(name=region_num,N=random.randint(500,5000)))
                region_num += 1
            self.regions.append(row_array)
​
    def tick_time(self):
        reports = []
        for i in range(0, self.rows):
            row_reports = []
            for j in range(0, self.columns):
                row_reports.append(self.regions[i][j].tick_time())
            reports.append(row_reports)
        return self.get_state_report(reports), reports
​
    def get_state_report(self, reports):
        state_report = None
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if state_report is None:
                    state_report = reports[i][j]
                else:
                    state_report = state_report + reports[i][j]
        return state_report
​
​
​
​
​
state = StateModel(10,10)
for i in range(0,30):
    sr, rr = state.tick_time()
print(sr)
print(rr)