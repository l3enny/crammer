from constants import *

# Unnecessary, but convenient values
Tg = 300                             # neutral gas temperature, J
P = 3.0 * 133.322                    # neutral gas pressure, Pa
EN = 1.0e-16 * 1e-4                  # reduced electric field, V m^2

#  Physical system options (user-defined)
Te = 0.5 * q                         # effective electron temperature, J
Ng = P/(kB*Tg)                       # neutral gas density, 1/m^3
E0 = EN * Ng                         # The applied electric field
M = 4.002602 * amu                   # Mass of the neutral particle

# WARNING: This value is worthless for the current equilibrium solver
ne = 1e5 * 1e6                       # background electron density, 1/m^3

# Solver options (user-defined)
T = 2.0e-7          # duration to simulate, s
hmin = 1e-18        # minimum time step, s
hmax = 1e-09        # maximum time step, s
dt = 1e-16
tau = 1e-9
TOL = 1.0e-06       # absolute allowable truncation error, 1/m^3

# Output options (user-defined)
dumprate = 0        # write data to disk after this many steps, 0 = never
prefix = 'dump'     # file prefix for data files
