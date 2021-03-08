class Report:

    def __init__(self, region, population, infected, dead, susceptible, recovered, beta, day):
        self._region = region
        self._population = population
        self._infected = infected
        self._dead = dead
        self._susceptible = susceptible
        self._recovered = recovered
        self._beta = beta
        self._day = day

    def get_region(self):
        return self._region

    def get_population(self):
        return self._population

    def get_infected(self):
        return self._infected

    def get_dead(self):
        return self._dead

    def get_susceptible(self):
        return self._susceptible

    def get_recovered(self):
        return self._recovered

    def get_beta(self):
        return self._beta

    def get_day(self):
        return self._day

    def __str__(self):
        return \
            "Region : " + str(self._region) + '\n' + \
            "Population : " + str(self._population) + '\n' + \
            "Infected : " + str(self._infected) + '\n' + \
            "Dead : " + str(self._dead) + '\n' + \
            "Susceptible : " + str(self._susceptible) + '\n' + \
            "Recovered : " + str(self._recovered) + '\n' + \
            "Beta : " + str(self._beta) + '\n' + \
            "Day : " + str(self._day) + '\n'
            
    def __add__(self, other):
        name = -2 # Invalid Report
        if self._day == other.get_day() and self._region != -2 and other.get_region() != -2:
            name = -1 # Valid Report
        return Report(name,
                      self._population + other.get_population(),
                      self._infected + other.get_infected(),
                      self._dead + other.get_dead(),
                      self._susceptible + other.get_susceptible(),
                      self._recovered + other.get_recovered(),
                      (self._beta + other.get_beta())/2,
                      self._day)
