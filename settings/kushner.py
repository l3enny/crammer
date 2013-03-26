from constants import *

# Unnecessary, but convenient values
Tg = 300                             # neutral gas temperature, J
P = 2.0 * 133.322                    # neutral gas pressure, Pa
EN = 3.00e-18 * 1e-4                 # reduced electric field, V m^2

#  Physical system options (user-defined)
Te = 1.620e-1 * q / kB                # effective electron temperature, K
Ng = P/(kB*Tg)
E0 = EN * Ng                         # The applied electric field
tau = 0
M = 4.002602 * amu                   # Mass of the neutral particle
ne = 6.436e7 * 1e6                   # background electron density, 1/m^3

# Solver options (user-defined)
T = 1.0e-08         # duration to simulate, s
dt = 1e-10          # solution time step
TOL = 1.0e-06       # absolute allowable truncation error, 1/m^3

# Output options (user-defined)
prefix = 'dump'     # file prefix for data files
equalize = False # Solve for equilibrium densities; ignores ne
energy = False      # Track the energy evolution
