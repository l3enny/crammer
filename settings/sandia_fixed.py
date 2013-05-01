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
Te = 6.5 * q / kB                    # initial electron temperature, K
P = 4.0 * 133.322                    # neutral gas pressure, Pa
Ng = P/(kB*Tg)                       # gas density, 1/m^3
M = 4.002604 * amu                   # mass of the neutral particle
ne = 5.363255e13                     # initial electron density, 1/m^3

# Solver options (user-defined)
T = 1.7e-7          # duration to simulate, s
dt = 1e-10          # time step size, s

# Applied electric field function
def Ef(t):
    return 0.0

# Output options (user-defined)
prefix = 'dump'     # file prefix for data files
energy = False

# Broken options!
equalize = False    # sets 
