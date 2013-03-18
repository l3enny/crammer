"""
Main script for running CRM simulation. The code is written in a frame-
work manner allowing the user some flexibility in how the problem is
solved. I don't have a lot of time for comprehensive documentation so
this script will be heavily commented to compensate.

Requirements: Numpy 1.6+, Scipy 0.10+
"""

# Standard Modules
from datetime import datetime

# Third Party Modules
import numpy as np
from scipy.integrate import odeint

# Included Modules
from constants import *     # Useful elementary constants
import handler              # Input/output handling
import initcond             # Helpful functions for initial conditions
import matrixgen            # Generates the rate matrices
import rate                 # Determines reaction rates
import solvers              # Handles general state calculations

# User-specified options
from settings import *               # load user settings file
from gases import helium as gas      # choose gas to simulate


# Convenient localization of state information, and ordering in 
# ascending energy.
# TODO: This is a bit inelegant; there should be a better way to do this
states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])

# Generate steady state transition matrices and radiation matrix
Ae = matrixgen.electronic(gas, dist, Te)
Ao = matrixgen.optical(gas)

# Define the rate equation
# TODO: Should this be a user setting as well?
def dNdt(t):
    # Atomic populations equation
    return Ae*ne + Ao

def dTdt(t):
    # Electron energy equation
    return q**2 * ne * E**2 / (me * km * N) \
           - ne * (2 * me / M) * km * N * 1.5 * kB * (Te - Tg) \
           - ne * N * k * dE

# Set the initial conditions
# TODO: Make this a user setting
N = initcond.equilibrium(dNdt(0.0)) * Ng
ne = N[-1] # ensure quasi-neutrality, assumes ion is last state

# Function to append emissions values for each time step
def rad(A, N, dt):
    emits = np.array([])
    for row in range(A.shape[0] - 1):
        i = row + 1
        emits = np.append(emits, A[row][i:] * N[i:] * dt)
    return emits
    
# Initialize solution arrays
Arad = Ao.clip(min=0)
errors = [0.0]
populations = [N]
times = [0.0]
emissions = [np.zeros(np.count_nonzero(Arad))]

# Initialize solver and evolve states over time
dNdt = solvers.rkf45(dNdt, times[0], populations[0], hmax, hmin, TOL)
dTdt = solvers.rkf45(dTdt, times[0], populations[0], hmax, hmin, TOL)
start = datetime.now()
while times[-1] < T:
    k = rates()
    N, t, eps = dNdt.next()  # Step to next value with generator function
    T, t, eps = dTdt.next()  # Step to next value with generator function
    # Using python lists, append is much faster than NumPy equivalent
    emissions.append(rad(Arad, N, t - times[-1]))
    populations.append(N)
    times.append(t)
    errors.append(eps)
    if 'ion' in states:
        ne = N[-1]  # increase electron density to account for ionization

    # Output some useful information every 1000 steps
    if len(times)%1000 == 0:
        end = datetime.now()
        print "%g steps" % len(times)
        print "Elapsed time:", times[-1]
        print "Simulation Time:", (end - start), "\n"

# Generate all emission wavelengths
wavelengths = solvers.wavelengths(states, order)
# Move populations to an array for proper output
populations = np.array(populations)
handler.save([times, populations, errors, emissions, wavelengths], prefix)
