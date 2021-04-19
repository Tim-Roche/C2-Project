class Report:

    def __init__(self, region, population, infected, dead, susceptible, recovered, vaccinated,
                 pfizer, moderna, beta, r, gamma, rollingSevenDays_P, rollingSevenDays_M, isSmallRegion, distroLimit,d_inf, day):
        self._region = region
        self._population = population
        self._infected = infected
        self._dead = dead
        self._d_inf = d_inf
        self._susceptible = susceptible
        self._recovered = recovered
        self._vaccinated = vaccinated
        self._pfizer = pfizer
        self._moderna = moderna
        self._beta = beta
        self._day = day
        self._available_pfizer = 0
        self._available_moderna = 0
        self._rollingSevenDays_P = rollingSevenDays_P
        self._rollingSevenDays_M = rollingSevenDays_M
        self._r = r
        self._gamma = gamma
        self._isSmallRegion = isSmallRegion
        self._distroLimit = distroLimit

    def get_distroLimit(self):
        return self._distroLimit

    def get_isSmallRegions(self):
        return self._isSmallRegion

    def get_d_inf(self):
        return self._d_inf

    def get_rollingSevenDays_P(self):
        return self._rollingSevenDays_P 

    def get_rollingSevenDays_M(self):
        return self._rollingSevenDays_M 

    def get_gamma(self):
        return self._gamma

    def get_r(self):
        return self._r

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

    def get_vaccinated(self):
        return self._vaccinated

    def get_pfizer(self):
        return self._pfizer

    def get_moderna(self):
        return self._moderna

    def get_beta(self):
        return self._beta

    def get_day(self):
        return self._day

    def get_available_pfizer(self):
        return self._available_pfizer

    def get_available_moderna(self):
        return self._available_moderna

    def set_available_pfizer(self, vac):
        self._available_pfizer = vac

    def set_available_moderna(self, vac):
        self._available_moderna = vac

    def __str__(self):
        return \
            "Region : " + str(self._region) + '\n' + \
            "isSmallRegion: " + str(bool(self._isSmallRegion)) + '\n' + \
            "Population : " + str(self._population) + '\n' + \
            "Infected : " + str(self._infected) + '\n' + \
            "Dead : " + str(self._dead) + '\n' + \
            "Susceptible : " + str(self._susceptible) + '\n' + \
            "Recovered : " + str(self._recovered) + '\n' + \
            "Vaccinated : " + str(self._vaccinated) + '\n' + \
            "Distributed Pfizer : " + str(self._pfizer) + '\n' + \
            "Distributed Moderna : " + str(self._moderna) + '\n' + \
            "RSD Pfizer: " + str(self._rollingSevenDays_P) + '\n' + \
            "RSD Moderna: " + str(self._rollingSevenDays_M) + '\n' + \
            "Available Pfizer : " + str(self._available_pfizer) + '\n' + \
            "Available Moderna : " + str(self._available_moderna) + '\n' + \
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
                      self._vaccinated + other.get_vaccinated(),
                      self._pfizer + other.get_pfizer(),
                      self._moderna + other.get_moderna(),
                      
                      (self._beta + other.get_beta())/2,
                      (self._r + other.get_r())/2,
                      (self._gamma + other.get_gamma())/2,
                      self._rollingSevenDays_P + other.get_rollingSevenDays_P(),
                      self._rollingSevenDays_M + other.get_rollingSevenDays_M(),
                      False,
                      (self._distroLimit + other.get_distroLimit()) / 2,
                      False,
                      self._day)
                      
