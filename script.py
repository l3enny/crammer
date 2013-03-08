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
import distributions        # Module containing various distributions
import handler              # Input/output handling
import matrixgen            # Generates the rate matrices
import rate                 # Determines reaction rates
import solvers              # Handles general state calculations

# User-specified options
from settings import *               # load user settings file
from gases import helium as gas      # choose gas to simulate


# Provide access to gas state information and matrix state order
states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])

# Generate steady state transition matrices and radiation matrix
Ae = matrixgen.electronic(gas, dist, Te)
Ao = matrixgen.optical(gas)
Aa = matrixgen.atomic(gas

# Generate all emission wavelengths
wavelengths = np.array([])
for istate in order:
    Ei = states[istate]['E']
    for fstate in [i for i in order if i != istate]:
        Ef = states[fstate]['E']
        if Ef < Ei:
            continue
        wavelengths = np.append(wavelengths, (h * c) / (Ef - Ei))
wavefile = open(prefix + '_wavelengths.csv', 'w')
np.savetxt(wavefile, wavelengths, delimiter=',')
wavefile.close()

# Solve for equilibrium
Ng = Na * 8.314 * Tg/P
eqerr = 1.0
n = ne
while eqerr > TOL:
    N = solvers.equilibrium(Ae*ne + Ao + Aa*Ng) * Ng
    eqerr = abs(n - N[-1]) / N[-1]
    n = N[-1]

# Initialize arrays with appropriate starting values
populations = [N]
times = [0.0]
errors = [0.0]
emissions = [np.zeros(sum(range(1, len(order))))]

# Define rate equation
def f(t, y):
    # Include any time dependent perturbations here
    rates = np.dot((Ae*ne + Ao + Aa*Ng), y)
    return rates

def rad(A, N, dt):
    emits = np.array([])
    for row in range(A.shape[0] - 1):
        i = row + 1
        emits = np.append(emits, A[row][i:] * N[i:] * dt)
    return emits
    
# Initialize solver and evolve states over time
Arad = np.fill_diagonal(Ao.copy(), 0)
stepper = solvers.rkf45(f, times[0], populations[0], hmax, hmin, TOL)
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

populations = np.array(populations)
handler.save(fids, times, populations, errors, emissions)
