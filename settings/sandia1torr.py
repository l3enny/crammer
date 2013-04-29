from constants import *

# Unnecessary, but convenient values
P = 1.0 * 133.322                    # neutral gas pressure, Pa

# Physical Parameters
M = 4.002602 * amu                   # Mass of the neutral particle, kg
Tg = 300                             # neutral gas temperature, K
Ng = P/(kB*Tg)                       # neutral gas density, 1/m^3
Te = 0.2 * q / kB                    # initial electron temperature, K
ne = 2.229503e11                     # initial electron density, 1/m^3

# Wave front parameters
tau = 1e-8                           # length of pulse, s
E0 = 9e1 / 0.01                      # applied electric field, V/m

# Solver options
T = 1.4e-7          # duration to simulate, s
dt = 1e-10          # time step for simulation, s

# Output options
prefix = 'dump'     # file prefix for data files
equalize = False    # starts simulation with excited states in equilibrium
energy = True       # conserves energy density of electrons
