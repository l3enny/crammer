"""
Main script for running CRM simulation. The code is written in a frame-
work manner allowing the user some flexibility in how the problem is
solved. I don't have a lot of time for comprehensive documentation so
this script will be heavily commented to compensate.

Requirements: Numpy 1.6+, Scipy 0.10+
"""

# Standard Modules
from datetime import datetime
import csv

# Third Party Modules
import numpy as np

# Included Modules
from constants import *     # Useful elementary constants
import handler              # Input/output handling
import matrixgen            # Generates the rate matrices
import solvers              # Handles general state calculations

# User-specified options
from settings.sandia import *       # load user settings file
from gases import helium as gas      # choose gas to simulate

# Convenient localization of state information, and ordering in 
# ascending energy.
# TODO: This is a bit inelegant; there should be a better way to do this
states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])

print "The applied electric field is: %g V/m" % E0

# Generate initial transition matrices and constants
Ao = matrixgen.optical(gas)
Alin = matrixgen.linopt(gas)
Ae = matrixgen.electronic(gas, Te)
km = matrixgen.km(gas, Te)
dE = solvers.dE(states, order)

def dNdt(t, N):
    term = np.dot(Ae*ne + Ao, N)
    return term

def dTedt(t, Te):
    if t < tau:
        E = E0
    else:
        E = 0
    source = q**2 * ne * E**2 / (me * km * Ng)
    elastic = - ne * km * Ng * (2 * me / M) * 1.5 * kB * (Te - Tg)
    inelastic = - np.sum(np.dot(ne * Ae * dE, N))
    return (source + elastic + inelastic) * (2./3) / (kB * ne)

# Calculate the equilibrium condition
if equalize:
    ierr = 1.0
    iTOL = 1.0e-6
    n = ne
    while ierr > iTOL:
        N = solvers.svd(Ae*n + Ao) * Ng
        print "N =", N
        raw_input('')
        ierr = abs(n - N[-1]) / N[-1]
        n = N[-1]
    N = N
    ne = N[-1]
else:
    N = np.array([Ng - ne, 0, 0, 0, 0, 0, 0, ne])

# Initialize solution arrays
errors = [0.0]
populations = [N]
times = [0.0]
emissions = [np.zeros(Alin.shape)]
temperatures = [Te]

# Solution loop
start = datetime.now()
while times[-1] < T:
    N = solvers.rk4(dNdt, times[-1], N, dt).clip(min=0)
    if energy:
        Te = solvers.rk4(dTedt, times[-1], Te, dt) # Advance with same time step
    else:
        pass
    ne = N[-1]
    # There must be a more elegant way of accomplishing this ...
    Nalign = []
    for i in range(1, len(N)):
        Nalign.extend([N[i]] * i)
    # Python lists are much faster than appending to ndarrays
    emissions.append(Alin * Nalign * dt)
    populations.append(N)
    times.append(times[-1] + dt)
    temperatures.append(Te)

    # Regenerate temperature-dependent quantities
    Ae = matrixgen.electronic(gas, Te)
    km = matrixgen.km(gas, Te)

    # Output some useful information every 1000 steps
    if len(times)%1000 == 0:
        end = datetime.now()
        print "%g steps" % len(times)
        print "Te =", Te
        print "Simulation time: %g (%g)" % (times[-1], T)
        print "Elapsed Time:", (end - start), "\n"

# Generate all emission wavelengths in the proper order
wavelengths = solvers.wavelengths(states, order)
order = np.array(order)
names = ['times', 'populations', 'wavelengths', 'temperatures', 'emissions']
data =  [times, populations, wavelengths, temperatures, emissions]
# Replace the order dump with something a tad more elegant
with open('dump_order.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(order)
handler.save(data, names, prefix)
