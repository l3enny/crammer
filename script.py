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
N[0] = Ng - n_e              # correct for fractional ionization
N[1] = Nm0                   # override with measured metastables
N[-1] = n_e                  # override with measured electrons

# Generate emission wavelengths and factors for trapping
l = solvers.wavelengths(states, order)
g = matrixgen.g_ratio(gas)
v_th = np.sqrt(k * Tg / M)

# Generate initial transition matrices and constants
# Option to include radiation trapping
if trapping:
    Ao = matrixgen.optical(gas)
    k0 = g * l**3 * N * Ao / (8 * pi * pi**0.5 * v_th)      
    T_f = k0 * R * np.sqrt(pi * np.log(k0 * R)) / 1.6
    T_f[np.isnan(T_f)] = 1.0
    Ao *= T_f
else:
    Ao = matrixgen.optical(gas)
allowed = Ao > 0.0
Aa = matrixgen.atomic(gas)
dE = solvers.dE(states, order)
E = np.array([states[i]['E'] for i in order])
Ae = matrixgen.electronic(gas, coeffs, Te)

def dNdt(t, N):
    term = np.dot(Ae*n_e + Ao + Aa * Ng, N)
    return term

def dn_edt(t, n_e):
    S = Ae[-1, :-1]
    alpha_cr = S * N[:-1] / (n_e * N[-1])
    test = n_e**2 * alpha_cr * N[-1]
    pass

def dTedt(t, Te):
    source = e**2 * n_e * Ef(t)**2 / (m_e * km(Te) * Ng)
    elastic = - 3 * n_e * km(Te) * Ng * (m_e / M) * 1.5 * k * (Te - Tg)
    inelastic = - np.sum(np.dot(n_e * Ae * dE, N))
    return (source + elastic + inelastic) * (2./3) / (k * n_e)

# Initialize solution arrays
errors = [0.0]
populations = [N]
emissions = [np.zeros(len(l[allowed]))]
temperatures = [Te]
field = [0.0]
times = [0.0]
energies = [np.sum(N * E + 1.5 * k * Te * n_e)]
coupled = [0.0]

# Solution loop
start = datetime.now()
steps = 0
while times[-1] < T:
    # Integrate population (and energy) equations.
    N = solvers.rk4(dNdt, times[-1], N, dt)
    N = N.clip(min=0)
    times.append(times[-1] + dt)

    # Option to include radiation trapping
    if trapping:
        Ao = matrixgen.optical(gas)
        k0 = g * l**3 * N * Ao / (8 * pi * pi**0.5 * v_th)      
        T_f = k0 * R * np.sqrt(pi * np.log(k0 * R)) / 1.6
        T_f[np.isnan(T_f)] = 1.0
        Ao *= T_f

    # Option to track energy evolution
    if energy:
        Te = solvers.rk4(dTedt, times[-1], Te, dt)
        Ae = matrixgen.electronic(gas, coeffs, Te)

    n_e = N[-1]          # enforce quasi-neutrality

    # Generate the relevant initial atomic states for emission calc
    Nalign = np.ones((dim, dim))
    Nalign = Nalign * N.T
    Nalign = Nalign[allowed]

    # NB: Appending to lists much faster than appending to arrays
    emissions.append(Ao[allowed] * Nalign * dt)
    populations.append(N)
    temperatures.append(Te)
    field.append(Ef(times[-1]))
    energies.append(np.sum(N*E) + 1.5 * k * Te * n_e)
    coupled.append(dt * e**2 * n_e * Ef(times[-1])**2 /
                   (m_e * km(Te) * Ng) + coupled[-1])
    steps += 1

    # Output some useful information when requested
    if steps%infostep == 0:
        end = datetime.now()
        print "Simulation time: %g s of %g s" % (times[-1], T)
        print "Elapsed Time:", (end - start)
        print "Triplet metastable density:", N[1]
        print "Te = %e eV\n" % (Te * k / e)

print "Final triplet metastable density:", N[1]

order = np.array(order)
names = ['times', 'populations', 'wavelengths', 'temperatures', 'emissions',
         'energies', 'field', 'coupled']
data =  [times, populations, l[allowed], temperatures, emissions, energies,
         field, coupled]
# Replace the order dump with something a tad more elegant
with open(prefix + '_order.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(order)
handler.save(data, names, prefix)
