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
import matrixgen            # Generates the rate matrices
import solvers              # Handles general state calculations

# User-specified options
from settings.kushner import *       # load user settings file
from gases import helium as gas      # choose gas to simulate

# Convenient localization of state information, and ordering in 
# ascending energy.
# TODO: This is a bit inelegant; there should be a better way to do this
states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])

# Initial transition matrix conditions
# TODO: Make this a user setting
Ao = matrixgen.optical(gas)
Ae = matrixgen.electronic(gas, Te)      # Generate electron rates
print "Ae =", Ae
import matplotlib.pyplot as plt
plt.contourf(Ae)
plt.colorbar()
plt.show()
raw_input('')
km = matrixgen.km(gas, Te)/2.688e25     # Generate momentum transfer
def dNdt(t, N):
    # Atomic populations equation
    term = np.dot(Ae*ne + Ao, N)
    return term

dE = solvers.dE(states, order)
def dTedt(t, Te):
    # Electron energy equation
    if t < tau:
        E = E0
    else:
        E = 0
    source = q**2 * ne * E**2 / (me * km * Ng)
    elastic = - ne * km * Ng * (2 * me / M) * 1.5 * kB * (Te - Tg)
    inelastic = - np.sum(np.dot(ne * Ae * dE, N))
    print "source =", dt * (2./3) * source / (kB * ne), "(K)"
    print "elastic=", dt * (3./3) * elastic / (kB * ne), "(K)"
    print "inelastic=", dt * (2./3) * inelastic / (kB * ne), "(K)"
    raw_input('')
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
Arad = Ao.clip(min=0)   # Removes depopulation component
errors = [0.0]
populations = [N]
times = [0.0]
emissions = [np.zeros(Arad.shape)]
temperatures = [Te]

# Solution loop
#stepper = solvers.rkf45(dNdt, times[0], populations[0], hmax, hmin, TOL)
start = datetime.now()
while times[-1] < T:
    ne = N[-1]
    N = solvers.rk4(dNdt, times[-1], N, dt).clip(min=0)
    print "N =", N
    #N, dt, eps = stepper.next()  # Step to next value with generator function
    if energy:
        Te = solvers.rk4(dTedt, times[-1], Te, dt) # Advance with same time step
        print "New Te =", Te
    else:
        pass
    # Using python lists, append is much faster than NumPy equivalent
    emissions.append(Arad * N * dt) #TODO: Verify that this works!
    populations.append(N)
    times.append(times[-1] + dt)
    #errors.append(eps)
    temperatures.append(Te)

    # Regenerate temperature-dependent quantities
    Ae = matrixgen.electronic(gas, Te)
    km = matrixgen.km(gas, Te)/2.688e25    # Generate momentum transfer


    # Output some useful information every 1000 steps
    if len(times)%1000 == 0:
        end = datetime.now()
        print "%g steps" % len(times)
        print "Te =", Te
        print "Simulation time:", times[-1], "(dt = %e s)" % (times[-1] -
                times[-2])
        print "Elapsed Time:", (end - start), "\n"

# Generate all emission wavelengths in the proper order
wavelengths = solvers.wavelengths(states, order)
# Move populations to an array for proper output (is this necessary?)
# populations = np.array(populations)
names = ['times', 'populations', 'errors', 'wavelengths', 
         'temperatures', 'emissions']
data =  [times, populations, errors, wavelengths, temperatures, emissions]
handler.save(data, names, prefix)
