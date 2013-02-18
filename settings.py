#  Physical system options (user-defined)
Te = 1.0 * q                         # effective electron temperature, J
dist = distributions.drumax(0.5, Te) # load EEDF
ne = 1e10 * 1e6                      # background electron density, 1/m^3
Tg = 300                             # neutral gas temperature, K
P = 10.0 * 133.322                   # neutral gas pressure, Pa

# Solver options (user-defined)
T = 0.3e-6          # duration to simulate, s
hmin = 1e-18        # minimum time step, s
hmax = 1e-09        # maximum time step, s
TOL = 1.0e-06       # absolute allowable truncation error, 1/m^3

# Output options (user-defined)
dumprate = 0        # write data to disk after this many steps, 0 = never
prefix = 'dump'     # file prefix for data files
