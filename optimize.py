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
from scipy import optimize
from scipy.constants import k, e

# Included Modules
import handler              # Input/output handling
import matrixgen            # Generates the rate matrices
import rates
import solvers              # Handles general state calculations

# User-specified options
from settings.s8torr import *       # load user settings file

# Convenient localization of state information, and ordering in 
# ascending energy.
# TODO: This is a bit inelegant; there should be a better way to do this
states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])

# Generate statics transition matrices
Ao = matrixgen.optical(gas)
Alin = matrixgen.linopt(gas)
Ae = matrixgen.electronic2(gas, coeffs, Te)
dE = solvers.dE(states, order)
E = np.array([states[i]['E'] for i in order])

def dNdt(t, N):
    term = np.dot(Ae*ne + Ao, N)
    return term

def dTedt(t, Te):
    source = e**2 * ne * Ef(t)**2 / (me * km(Te) * Ng)
    elastic = - ne * km(Te) * Ng * (3 * me / M) * 1.5 * k * (Te - Tg)
    inelastic = - np.sum(np.dot(ne * Ae * dE, N))
    return (source + elastic + inelastic) * (2./3) / (k * ne)

def integrate(times, solver):

    # Initialize solution arrays
    populations = [N]
    emissions = [np.zeros(Alin.shape)]
    temperatures = [Te]
    field = [0.0]
    energies = [np.sum(N * E + 1.5 * k * Te * ne)]

    # Solution loop
    start = datetime.now()
    prev = times[0]
    for t in times[1:]:

        dt = t - prev

        # Integrate population (and energy) equations.
        N = solver(dNdt, t, N, dt).clip(min=0)
        if energy:
            Te = solver(dTedt, t, Te, dt).clip(min=0)
            Ae = matrixgen.electronic2(gas, coeffs, Te)

        ne = N[-1]          # enforce quasi-neutrality
        prev = t

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

def simulate(times, N_meas, E0, delay):
    dt = 4e-10
    def Ef(t):
        a = E0
        b = delay
        c = tau / (2 * sqrt(2 * log(2)))
        return a * exp(-(t - b)**2 / (2 * c**2))
    return integrate(times, N_shift)


guesses = (1e2 / 1e-2, 40e-9)
optimize.curve_fit(simulate, times, N_meas, p0=guesses)

# Generate all emission wavelengths in the proper order
wavelengths = solvers.wavelengths(states, order)
order = np.array(order)
names = ['times', 'populations', 'wavelengths', 'temperatures', 'emissions',
'energies', 'field']
data =  [times, populations, wavelengths, temperatures, emissions, energies,
        field]

# Replace the order dump with something a tad more elegant
with open(prefix + '_order.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(order)
handler.save(data, names, prefix)
