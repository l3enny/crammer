"""
Main script for running CRM simulation. The code is written in a frame-
work manner allowing the user some flexibility in how the problem is
solved. I don't have a lot of time for comprehensive documentation so
this script will be heavily commented to compensate.

Requirements: Numpy 1.6+, Scipy 0.10+
"""

# Standard Modules
import csv
from datetime import datetime
from math import pi

# Third Party Modules
import numpy as np
from scipy.constants import k, e, m_e

# Included Modules
import handler              # Input/output handling
import matrixgen            # Generates the rate matrices
import rates
import solvers              # Handles general state calculations

# User-specified options
from settings.s1torr import *       # load user settings file

# Convenient localization of state information, and ordering in 
# ascending energy.
# TODO: This is a bit inelegant; there should be a better way to do this
states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])
dim = len(states)

# Set initial atomic densities
N = np.array(Ni, ndmin=2).T  # load equilibrium dist. from settings
N[0] = Ng - ne               # correct for fractional ionization
N[1] = Nm0                   # override with measured metastables
N[-1] = ne                   # override with measured electrons

# Generate emission wavelengths and factors for trapping
l = solvers.wavelengths(states, order)
g = matrixgen.g_ratio(gas)
v_th = np.sqrt(k * Tg / M)

# Generate initial transition matrices and constants
Ao = matrixgen.optical(gas)
allowed = Ao > 0.0
Ao_allowed = Ao[allowed]
l_allowed = l[allowed]
Aa = matrixgen.atomic(gas)
dE = solvers.dE(states, order)
E = np.array([states[i]['E'] for i in order])
Ae = matrixgen.electronic(gas, coeffs, Te)
# Option to include radiation trapping
if trapping:
    k0 = g * l**3 * N * Ao / (8 * pi * pi**0.5 * v_th)      
    T_f = k0 * R * np.sqrt(pi * np.log(k0 * R)) / 1.6
    T_f[np.isnan(T_f)] = 1.0
    Ae *= T_f

def dNdt(t, N):
    term = np.dot(Ae*ne + Ao + Aa * Ng, N)
    return term

def dTedt(t, Te):
    source = e**2 * ne * Ef(t)**2 / (m_e * km(Te) * Ng)
    elastic = - 3 * ne * km(Te) * Ng * (m_e / M) * 1.5 * k * (Te - Tg)
    inelastic = - np.sum(np.dot(ne * Ae * dE, N))
    return (source + elastic + inelastic) * (2./3) / (k * ne)

# Initialize solution arrays
errors = [0.0]
populations = [N]
emissions = [np.zeros(len(l_allowed))]
temperatures = [Te]
field = [0.0]
times = [0.0]
energies = [np.sum(N * E + 1.5 * k * Te * ne)]
coupled = [0.0]

# Solution loop
start = datetime.now()
steps = 0
while times[-1] < T:
    # Integrate population (and energy) equations.
    N = solvers.rk4(dNdt, times[-1], N, dt)
    N = N.clip(min=0)
    times.append(times[-1] + dt)

    # Option to track energy evolution
    if energy:
        Te = solvers.rk4(dTedt, times[-1], Te, dt)
        Ae = matrixgen.electronic(gas, coeffs, Te)

        # Option to include radiation trapping
        if trapping:
            k0 = g * l**3 * N * Ao / (8 * pi * pi**0.5 * v_th)      
            T_f = k0 * R * np.sqrt(pi * np.log(k0 * R)) / 1.6
            T_f[np.isnan(T_f)] = 1.0
            Ae *= T_f

    ne = N[-1]          # enforce quasi-neutrality

    # Generate the relevant initial atomic states for emission calc
    Nalign = np.ones((dim, dim))
    Nalign = Nalign * N.T
    Nalign = Nalign[allowed]

    # Python lists are much faster than appending to ndarrays
    emissions.append(Ao_allowed * Nalign * dt)
    populations.append(N)
    temperatures.append(Te)
    field.append(Ef(times[-1]))
    energies.append(np.sum(N*E) + 1.5 * k * Te * ne)
    coupled.append(dt * e**2 * ne * Ef(times[-1])**2 /
                   (m_e * km(Te) * Ng) + coupled[-1])
    steps += 1

    # Output some useful information every 1000 steps
    if steps%1000 == 0:
        end = datetime.now()
        print "Te = %e eV" % (Te * k / e)
        print "Simulation time: %g s of %g s" % (times[-1], T)
        print "Elapsed Time:", (end - start), "\n"

print "Final triplet metastable density:", N[1]

order = np.array(order)
names = ['times', 'populations', 'wavelengths', 'temperatures', 'emissions',
         'energies', 'field', 'coupled']
data =  [times, populations, l_allowed, temperatures, emissions, energies,
         field, coupled]
# Replace the order dump with something a tad more elegant
with open(prefix + '_order.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(order)
handler.save(data, names, prefix)
