from constants import *

# Unnecessary, but convenient values
Tg = 300                             # neutral gas temperature, J
P = 2.0 * 133.322                    # neutral gas pressure, Pa
EN = 2.66e-15 * 1e-4                 # reduced electric field, V m^2

#  Physical system options (user-defined)
Te = 1.818e1 * q / kB                # effective electron temperature, K
Ng = P/(kB*Tg)
E0 = EN * Ng                         # The applied electric field
tau = 0
M = 4.002602 * amu                   # Mass of the neutral particle

# WARNING: This value is worthless for the current equilibrium solver
ne = 1.670e14                        # background electron density, 1/m^3

# Solver options (user-defined)
T = 1.0e-14         # duration to simulate, s
hmin = 1e-20        # minimum time step, s
hmax = 1e-09        # maximum time step, s
dt = 1e-16
TOL = 1.0e-06       # absolute allowable truncation error, 1/m^3

# Output options (user-defined)
prefix = 'dump'     # file prefix for data files
