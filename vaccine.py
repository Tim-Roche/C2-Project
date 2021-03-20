class vaccine():
    def __init__(self, name, vaccineCount=0):
        self.vaccineCount = vaccineCount
        self.name = name
        self.vac_q = []
        
    def vaccinate(self,num):
        self.vaccineCount -= num
        print("---" + self.name + "---")
        print("Vaccinated " + str(num) + " poeple")
        print("Remaining: " + str(self.vaccineCount))


    def addToQueue(self, d_vacA):
        self.vac_q.append(d_vacA)

    def frontOfLine(self):
        return(float(self.vac_q[:1][0]))

    def pop(self, remaining=0):
        self.vac_q = self.vac_q[1:]
        self.vac_q[-1] += remaining

    def addVaccines(self, vaccines):
        self.vaccineCount+=vaccines

    def queueLength(self):
        return(len(self.vac_q))

    def remainingVaccines(self):
        return(self.vaccineCount)