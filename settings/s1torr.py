from scipy.constants import e, k
import numpy as np
from numpy import exp, sqrt, log, maximum, minimum
from gases import helium as gas      # choose gas to simulate
import cPickle

with open('./gases/helium/pack_1p0.pickle', mode='r') as f:
    pack = cPickle.load(f)

# Function containing momentum transfer rate coefficient, accepts temperature
# as a input, produces rate coefficient in m^3/s
km = pack.km

with open('./gases/helium/combined.pickle', mode='r') as f:
    coeffs = cPickle.load(f)

T = 1.9e-7          # duration to simulate, s
dt = 5e-12          # target step time

# Output options (user-defined)
prefix = '1torr'    # file prefix for data files
energy = True       # track electron energy changes
trapping = True     # radiation trapping for excited states

# Physical system options (user-defined)
Tg = 300                            # neutral gas temperature, K
Te = 0.2 * e / k                    # initial electron temperature, K
P = 1.0 * 133.322                   # neutral gas pressure, Pa
M = gas.constants.M                 # atomic mass, kg
R = 0.033 / 2                       # discharge radius (for trapping)
Ng = P/(k*Tg)                       # gas density, 1/m^3
ne = 2.229503e11                    # initial electron density, 1/m^3
Nm0 = 1.24e15 / 0.033
Ni = np.load("equilibrium.npy")

# Applied electric field function
E0 = 1.11295e2 / 1e-2   # amplitude
tau = 4.0e-8            # width
tail = 0.125            # tail fraction
t0 = 4.0e-8             # center

def E_gaussian(t):
    a = E0
    b = t0
    c = tau / (2 * sqrt(2 * log(2)))
    return a * exp(-(t - b)**2 / (2 * c**2))

Ef = E_gaussian
