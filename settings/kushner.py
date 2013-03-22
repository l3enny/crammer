from constants import *

# Unnecessary, but convenient values
Tg = 300                             # neutral gas temperature, J
P = 2.0 * 133.322                    # neutral gas pressure, Pa
EN = 2.66e-15 * 1e-4                 # reduced electric field, V m^2

#  Physical system options (user-defined)
Te = 1.818e1 * q                     # effective electron temperature, J
Ng = P/(kB*Tg)
E0 = EN * Ng                         # The applied electric field
tau = 0
M = 4.002602 * amu                   # Mass of the neutral particle

# WARNING: This value is worthless for the current equilibrium solver
ne = 1.670e14                        # background electron density, 1/m^3

# Solver options (user-defined)
T = 2.0e-6          # duration to simulate, s
hmin = 1e-18        # minimum time step, s
hmax = 1e-09        # maximum time step, s
TOL = 1.0e-06       # absolute allowable truncation error, 1/m^3

# Output options (user-defined)
dumprate = 0        # write data to disk after this many steps, 0 = never
prefix = 'dump'     # file prefix for data files
