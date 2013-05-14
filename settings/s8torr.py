from constants import *
from numpy import exp, sqrt, log, maximum, minimum
from gases import helium as gas      # choose gas to simulate
import cPickle

with open('./gases/helium/pack_m.pickle', mode='r') as f:
    pack = cPickle.load(f)

km = pack.km

with open('./gases/helium/ralchenko_m.pickle', mode='r') as f:
    coeffs = cPickle.load(f)

# Physical system options (user-defined)
Tg = 300                             # neutral gas temperature, K
Te = 0.2 * q / kB                    # initial electron temperature, K
P = 8.0 * 133.322                    # neutral gas pressure, Pa
Ng = P/(kB*Tg)                       # gas density, 1/m^3
M = 4.002604 * amu                   # mass of the neutral particle
ne = 1.161256e14                     # initial electron density, 1/m^3

# Solver options (user-defined)
T = 1.7e-7          # duration to simulate, s
dt = 1e-10          # time step size, s

# Applied electric field function
def Ef(t):
    E0 = a = 4.14e2 / 1e-2
    t0 = b = 4.0e-8
    tau = 3.5e-08
    c = tau / (2 * sqrt(2 * log(2)))
    return a * exp(-(t - b)**2 / (2 * c**2))
    #Ec = 0.125 * E0
    #return G + maximum(0, minimum(Ec, Ec/(2.*tau) * t + E0 * (tau -
    #    t0)/(2.*tau) ))

# Output options (user-defined)
prefix = '8torr'     # file prefix for data files
energy = True

# Broken options!
equalize = False    # sets 
