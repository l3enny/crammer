from constants import *

# Unnecessary, but convenient values
Tg = 300                             # neutral gas temperature, K
P = 3.0 * 133.322                    # neutral gas pressure, Pa
EN = 3.0e-16 * 1e-4                  # reduced electric field, V m^2

# Physical system options (user-defined)
# Electron temperature chosen for minimum of available data
Te = 0.2 * q / kB                    # effective electron temperature, K
Ng = P/(kB*Tg)                       # neutral gas density, 1/m^3
E0 = EN * Ng                         # The applied electric field
M = 4.002602 * amu                   # Mass of the neutral particle

# WARNING: This value is worthless for the current equilibrium solver
ne = 1e5 * 1e6                       # background electron density, 1/m^3

# Solver options (user-defined)
T = 2.8e-7          # duration to simulate, s
#hmin = 1e-18        # minimum time step, s
#hmax = 1e-09        # maximum time step, s
dt = 1e-10
tau = 5e-9
#TOL = 1.0e-06       # absolute allowable truncation error, 1/m^3

# Output options (user-defined)
prefix = 'dump'     # file prefix for data files
equalize = False
energy = True
