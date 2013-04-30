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
from constants import kB, q # Useful elementary constants
import handler              # Input/output handling
import matrixgen            # Generates the rate matrices
import rates
import solvers              # Handles general state calculations

# User-specified options
from settings.sandia import *       # load user settings file

# Convenient localization of state information, and ordering in 
# ascending energy.
# TODO: This is a bit inelegant; there should be a better way to do this
states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])

# Generate initial transition matrices and constants
Ao = matrixgen.optical(gas)
Alin = matrixgen.linopt(gas)
Ae = matrixgen.electronic2(gas, coeffs, Te)
#km = matrixgen.km(gas, Te)
dE = solvers.dE(states, order)
E = np.array([states[i]['E'] for i in order])

def dNdt(t, N):
    term = np.dot(Ae*ne + Ao, N)
    return term

def dTedt(t, Te):
    source = q**2 * ne * Ef(t)**2 / (me * km(Te) * Ng)
    elastic = - ne * km(Te) * Ng * (3 * me / M) * 1.5 * kB * (Te - Tg)
    inelastic = - np.sum(np.dot(ne * Ae * dE, N))
    return (source + elastic + inelastic) * (2./3) / (kB * ne)

# Calculate the equilibrium condition
#TODO: BROKEN!
if equalize:
    ierr = 1.0
    iTOL = 1.0e-6
    while ierr > iTOL:
        N = solvers.svd(Ae*ne + Ao) * Ng
        ierr = abs(ne - N[-1]) / N[-1]
        ne = N[-1]
else:
    N = np.zeros(len(states))
    N[0] = Ng - ne
    N[-1] = ne

# Initialize solution arrays
errors = [0.0]
populations = [N]
times = [0.0]
emissions = [np.zeros(Alin.shape)]
temperatures = [Te]
energies = [np.sum(N * E + 1.5 * kB * Te * ne)]

# Solution loop
start = datetime.now()
while times[-1] < T:

    # Integrate population (and energy) equations.
    N = solvers.rk4(dNdt, times[-1], N, dt).clip(min=0)
    if energy:
        Te = solvers.rk4(dTedt, times[-1], Te, dt)
        # Regenerate temperature-dependent quantities
        Ae = matrixgen.electronic2(gas, coeffs, Te)
        #km = matrixgen.km(gas, Te)

    ne = N[-1]          # enforce quasi-neutrality

    # There must be a more elegant way of accomplishing this ...
    Nalign = []
    for i in range(1, len(N)):
        Nalign.extend([N[i]] * i)

    # Python lists are much faster than appending to ndarrays
    emissions.append(Alin * Nalign * dt)
    populations.append(N)
    times.append(times[-1] + dt)
    temperatures.append(Te)
    energies.append(np.sum(N*E) + 1.5 * kB * Te * ne)

    # Output some useful information every 1000 steps
    if len(times)%1000 == 0:
        end = datetime.now()
        print "%g steps" % len(times)
        print "Te =", Te
        print "Simulation time: %g (%g)" % (times[-1], T)
        print "Elapsed Time:", (end - start), "\n"

print "Final triplet metastable density:", N[1]

# Generate all emission wavelengths in the proper order
wavelengths = solvers.wavelengths(states, order)
order = np.array(order)
names = ['times', 'populations', 'wavelengths', 'temperatures', 'emissions',
'energies']
data =  [times, populations, wavelengths, temperatures, emissions, energies]
# Replace the order dump with something a tad more elegant
with open('dump_order.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(order)
handler.save(data, names, prefix)
