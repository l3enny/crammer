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

# Included Modules
from constants import *     # Useful elementary constants
import handler              # Input/output handling
import matrixgen            # Generates the rate matrices
import rate                 # Determines reaction rates
import solvers              # Handles general state calculations

# User-specified options
from settings import *               # load user settings file
from gases import helium as gas      # choose gas to simulate


# Convenient localization of state information, and ordering in 
# ascending energy.
states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])

# Generate steady state transition matrices and radiation matrix
Ae = matrixgen.electronic(gas, dist, Te)
Ao = matrixgen.optical(gas)
Aa = matrixgen.atomic(gas)

# Define rate equation
def dfdt(t):
    return Ae*ne + Ao + Aa*Ng

# Set the initial conditions
times = [0.0]
emissions = [np.zeros(sum(range(1, len(order))))]
if 'ion' in states:
    populations = [solvers.ion_equilibrium(dfdt, Ng)]
else:
    populations = [solvers.svd(dfdt(0.0))]

# Function to append emissions values for each time step
def rad(A, N, dt):
    emits = np.array([])
    for row in range(A.shape[0] - 1):
        i = row + 1
        emits = np.append(emits, A[row][i:] * N[i:] * dt)
    return emits
    
# Initialize solver and evolve states over time
Arad = Ao.copy()
np.fill_diagonal(Arad, 0)
errors = [0.0]
stepper = solvers.rkf45(dfdt, times[0], populations[0], hmax, hmin, TOL)
start = datetime.now()
while times[-1] < T:
    N, t, eps = stepper.next()  # Step to next value with generator function
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
handler.save(prefix, [times, populations, errors, emissions, wavelengths])
