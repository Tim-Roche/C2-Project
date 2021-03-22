from RegionModel import RegionModel
from Report import Report
import random


class StateModel:
    def __init__(self, N, M):
        self._rows = N
        self._columns = M
        self._regions = []
        self._pfizer = 1000
        self._moderna = 1000
        self._init_regions()

    def _init_regions(self):
        region_num = 0
        for row in range(0, self._rows):
            row_array = []
            for col in range(0, self._columns):
                row_array.append(RegionModel(name=region_num, N=random.randint(500, 5000)))
                region_num += 1
            self._regions.append(row_array)

    def tick_time(self):
        reports = []
        for row in range(0, self._rows):
            row_reports = []
            for col in range(0, self._columns):
                row_reports.append(self._regions[row][col].tick_time())
            reports.append(row_reports)
        state_report = self.get_state_report(reports)
        state_report.set_available_pfizer(self._pfizer)
        state_report.set_available_moderna(self._moderna)
        if state_report.get_day() % 7 == 0:
            self._get_vaccines()
        return state_report, reports

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
        self._phizer += int((day/7)*1000)
        self._moderna += int((day/7)*1000)

    def distribute_vaccines(self, pfizer_plan, moderna_plan):
        prev_pfizer = self._pfizer
        prev_moderna = self._moderna
        for row in range(0, self._rows):
            for col in range(0, self._columns):
                d_pfizer = min(round(pfizer_plan[row][col]*prev_pfizer), self._phizer)
                d_moderna = min(round(moderna_plan[row][col]*prev_moderna), self._moderna)
                self._regions[row][col].vaccine_pfizer_count += d_pfizer
                self._regions[row][col].vaccine_moderna_count += d_moderna
                self._pfizer -= d_pfizer
                self._moderna -= d_moderna




state = StateModel(2,1)
for i in range(0,2):
    print("---- Time: " + str(i) + " ----")
    sr, rr = state.tick_time()
    print("State Report")
    print(sr)