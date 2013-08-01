from scipy.constants import e, k
import numpy as np
from numpy import exp, sqrt, log, maximum, minimum
from gases import helium as gas      # choose gas to simulate
import cPickle
import solvers

with open('./gases/helium/pack_1p0.pickle', mode='r') as f:
    pack = cPickle.load(f)

km = pack.km

with open('./gases/helium/combined.pickle', mode='r') as f:
    coeffs = cPickle.load(f)

solver = solvers.rk4

T = 1.9e-7          # duration to simulate, s

# Output options (user-defined)
prefix = '8torr'    # file prefix for data files
energy = True       # track electron energy changes

# Physical system options (user-defined)
Tg = 300                             # neutral gas temperature, K
Te = 0.2 * e / k                    # initial electron temperature, K
P = 8.0 * 133.322                    # neutral gas pressure, Pa
Ng = P/(k*Tg)                       # gas density, 1/m^3
M = 4.002604 * amu                   # mass of the neutral particle
ne = 1.161256e14                     # initial electron density, 1/m^3

# Applied electric field function
E0 = 5.11450e2 / 1e-2  # amplitude
tau = 2.0e-8            # width
tail = 0.125            # tail fraction
t0 = 4.0e-8             # center

def E_gaussian_tail(t):
    a = E0
    b = t0
    c = tau / (2 * sqrt(2 * log(2)))
    G = a * exp(-(t - b)**2 / (2 * c**2))
    Ec = E0 * tail
    return G + maximum(0, minimum(Ec, Ec/(2.*tau) * t \
           + E0 * (tau - t0)/(2.*tau) ))

def E_gaussian(t):
    a = E0
    b = t0
    c = tau / (2 * sqrt(2 * log(2)))
    return a * exp(-(t - b)**2 / (2 * c**2))

def E_tophat(t):
    if t0 - (tau/2) < t < t0 + (tau/2):
        return E0
    else:
        return 0.0

def E_tophat_tail(t):
    if t < t0 - (tau/2):
        return 0.0
    elif t >= t0 - (tau/2):
        return E0
    else:
        return E0 * tail
    
Ef = E_gaussian

# Broken options!
equalize = False    # sets 
