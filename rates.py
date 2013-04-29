from scipy.interpolate import UnivariateSpline

class Rates(object):
    def __init__(self, temperatures, rates, comments=None):
        if len(rates) != len(temperatures):
            raise ValueError('There must be an equal number of rate tables and',
            'temperatures.')
        self.rates = rates
        self.temperatures = temperatures
        self.comments = comments
    def rate(self, Te, i, f):
        #TODO: Store splines in memory for speedup
        select = []
        for table in self.rates:
            select.append(table[i][f])
        spline = UnivariateSpline(self.temperatures, select, s=0, k=2)
        return spline(Te)
    def km(self, Te):
        #TODO: Store splines in memory for speedup
        spline = UnivariateSpline(self.temperatures, self.rates, s=0, k=2)
        return spline(Te)
