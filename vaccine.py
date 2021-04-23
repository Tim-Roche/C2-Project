class vaccine():
    def __init__(self, name, vaccineCount=0):
        self.vaccineCount = vaccineCount
        self.vacsSecond = 0
        self.vacsFirst = 0
        self.name = name
        self.vac_q = []
        
    def vaccinate(self,num,secondDose=False):
        self.vaccineCount -= num
        if(secondDose):
            self.vacsSecond -= num
        else:
            self.vacsFirst -= num
        #print("---" + self.name + "---")
        #print("Vaccinated " + str(num) + " poeple")
        #print("Remaining: " + str(self.vaccineCount))

    def addToQueue(self, d_vacA):
        self.vac_q.append(d_vacA)

    def frontOfLine(self):
        return(float(self.vac_q[:1][0]))

    def rollingSevenDaySum(self):
        return(sum(self.vac_q[:7]))

    def pop(self, remaining=0):
        self.vac_q = self.vac_q[1:]
        self.vac_q[0] += remaining

    def addVaccines(self, vaccines, secondDose=False):
        #print(vaccines, secondDose)
        self.vaccineCount+=vaccines
        if(secondDose):
            self.vacsSecond+=vaccines
        else:
            self.vacsFirst+=vaccines

    def queueLength(self):
        return(len(self.vac_q))

    def remainingVaccines(self):
        return(self.vaccineCount)
    
    def remainingSecondDose(self):
        return(self.vacsSecond)
    
    def remainingFirstDose(self):
        return(self.vacsFirst)