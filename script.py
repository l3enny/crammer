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
from scipy.constants import k, e, m_e

# Included Modules
import handler              # Input/output handling
import matrixgen            # Generates the rate matrices
import rates
import solvers              # Handles general state calculations

# User-specified options
from settings.s4torr import *       # load user settings file

# Convenient localization of state information, and ordering in 
# ascending energy.
# TODO: This is a bit inelegant; there should be a better way to do this
states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])

# Generate initial transition matrices and constants
Ao = matrixgen.optical(gas)
Alin = matrixgen.linopt(gas)
Ae = matrixgen.electronic2(gas, coeffs, Te)
Aa = matrixgen.atomic(gas)
dE = solvers.dE(states, order)
E = np.array([states[i]['E'] for i in order])

def dNdt(t, N):
    term = np.dot(Ae*ne + Ao + Aa, N)
    return term

def dTedt(t, Te):
    source = e**2 * ne * Ef(t)**2 / (m_e * km(Te) * Ng)
    elastic = - 3 * ne * km(Te) * Ng * (m_e / M) * 1.5 * k * (Te - Tg)
    inelastic = - np.sum(np.dot(ne * Ae * dE, N))
    return (source + elastic + inelastic) * (2./3) / (k * ne)

N = Ni
N[0] = Ng - ne # correct for fractional ionization
N[1] = Nm0 # override with measured metastables
N[-1] = ne # override with measured electrons

# Initialize solution arrays
errors = [0.0]
populations = [N]
emissions = [np.zeros(Alin.shape)]
temperatures = [Te]
field = [0.0]
times = [0.0]
energies = [np.sum(N * E + 1.5 * k * Te * ne)]
coupled = [0.0]

# Solution loop
start = datetime.now()
solver = solvers.rkf45(dNdt, times[-1], N, dt * 1e6, dt * 1e-6, 1e-1)
steps = 0
while times[-1] < T:

    # Integrate population (and energy) equations.
    # N, dt, error = solver.next()
    N = solvers.rk4(dNdt, times[-1], N, dt)
    N = N.clip(min=0)
    times.append(times[-1] + dt)
    if energy:
        Te = solvers.rk4(dTedt, times[-1], Te, dt)
        # Regenerate temperature-dependent quantities
        Ae = matrixgen.electronic2(gas, coeffs, Te)

    ne = N[-1]          # enforce quasi-neutrality

    # There must be a more elegant way of accomplishing this ...
    Nalign = []
    for i in range(1, len(N)):
        Nalign.extend([N[i]] * i)

    # Python lists are much faster than appending to ndarrays
    emissions.append(Alin * Nalign * dt)
    populations.append(N)
    temperatures.append(Te)
    field.append(Ef(times[-1]))
    energies.append(np.sum(N*E) + 1.5 * k * Te * ne)
    coupled.append(dt * e**2 * ne * Ef(times[-1])**2 /
                   (m_e * km(Te) * Ng) + coupled[-1])
    steps += 1

    # Output some useful information every 1000 steps
    if steps%100 == 0:
        end = datetime.now()
        print "Te = %e eV" % (Te * k / e)
        print "Simulation time: %g s of %g s" % (times[-1], T)
        print "Elapsed Time:", (end - start), "\n"

print "Final triplet metastable density:", N[1]

# Generate all emission wavelengths in the proper order
wavelengths = solvers.wavelengths(states, order)
order = np.array(order)
names = ['times', 'populations', 'wavelengths', 'temperatures', 'emissions',
'energies', 'field', 'coupled']
data =  [times, populations, wavelengths, temperatures, emissions, energies,
        field, coupled]
# Replace the order dump with something a tad more elegant
with open(prefix + '_order.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(order)
handler.save(data, names, prefix)
