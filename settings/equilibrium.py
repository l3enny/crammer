from scipy.constants import e, k
import numpy as np
from numpy import exp, sqrt, log, maximum, minimum
from gases import helium as gas      # choose gas to simulate
import cPickle

with open('./gases/helium/pack_1p0.pickle', mode='r') as f:
    pack = cPickle.load(f)

km = pack.km

with open('./gases/helium/combined.pickle', mode='r') as f:
    coeffs = cPickle.load(f)

T = 1.0e-5          # duration to simulate, s

# Output options (user-defined)
prefix = '1torr_eq'  # file prefix for data files
energy = False       # track electron energy changes
trapping = True      # radiation trapping for excited states
infostep = 1000      # integer for number of steps per debug info

# Physical system options (user-defined)
Tg = 300                            # neutral gas temperature, K
Te = 0.2 * e / k                    # initial electron temperature, K
P = 1.0 * 133.322                   # neutral gas pressure, Pa
M = gas.constants.M
Ng = P/(k*Tg)                       # gas density, 1/m^3
ne = 2.229503e11                    # initial electron density, 1/m^3
Nm0 = 1.24e15
Ni = np.zeros(len(gas.states.states)) + 1

# Electric field function
Ef = lambda x: 0.0   # turn in off for simulation
