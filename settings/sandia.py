from constants import *
from numpy import exp, sqrt, log
from gases import helium as gas      # choose gas to simulate
import cPickle

with open('./gases/helium/pack.pickle', mode='r') as f:
    pack = cPickle.load(f)

km = pack.km

with open('./gases/helium/ralchenko.pickle', mode='r') as f:
    coeffs = cPickle.load(f)

# Physical system options (user-defined)
Tg = 300                             # neutral gas temperature, K
Te = 0.2 * q / kB                    # initial electron temperature, K
P = 4.0 * 133.322                    # neutral gas pressure, Pa
Ng = P/(kB*Tg)                       # gas density, 1/m^3
M = 4.002604 * amu                   # mass of the neutral particle
ne = 5.363255e13                     # initial electron density, 1/m^3

# Solver options (user-defined)
T = 1.7e-7          # duration to simulate, s
dt = 1e-10          # time step size, s
#TOL = 1.0e-06       # absolute allowable truncation error, 1/m^3
#hmin = 1e-18        # minimum time step, s
#hmax = 1e-09        # maximum time step, s

# Applied electric field function
#def Ef(t):
#    E0 = a = 3.10e2 / 1e-2
#    t0 = b = 2.0e-8
#    tau = 2.5e-08
#    c = tau / (2 * sqrt(2 * log(2)))
#    return a * exp(-(t - b)**2 / (2 * c**2))
def Ef(t):
    delay = 10.0e-9
    E0 = 2.71e2 / 1e-2
    tau = 2.5e-8
    if delay < t < tau + delay:
        return E0
    else:
        return 0.0

# Output options (user-defined)
prefix = 'dump'     # file prefix for data files
energy = True

# Broken options!
equalize = False    # sets 
