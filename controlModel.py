import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from RegionModel import RegionModel
from StateModel import StateModel
import time

class controlModel():
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.state = StateModel(self.rows,self.columns)

    def run(self):
        run = True
        while run:
            state_report, reports = self.state.tick_time()
            self.state.distribute_vaccines([[0.25,0.25],[0.25,0.25]], [[0.25,0.25],[0.25,0.25]])

            remaining = state_report.get_population() - (state_report.get_recovered() + state_report.get_vaccinated() + state_report.get_dead())
            
            if(remaining <= 0):
                run = False
                
            
            print("-----------")
            print(state_report)
            print()
            for rx in reports:
                for ry in rx:
                    print(ry)
            #        if ((ry.get_pfizer() - int(ry.get_pfizer())) != 0):
            #            run = False
            print(state_report.get_population() - (state_report.get_recovered() + state_report.get_vaccinated() + state_report.get_dead()))
            #time.sleep(0.1)

c = controlModel(2, 2)
c.run()
print("Done!")