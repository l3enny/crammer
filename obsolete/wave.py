"""
Main script for running CRM simulation. The code is written in a frame-
work manner allowing the user some flexibility in how the problem is
solved. I don't have a lot of time for comprehensive documentation so
this script will be heavily commented to compensate.

Requirements: Numpy 1.6+, Scipy 0.10+, Matplotlib 1.0+
"""

print "WARNING! This code is obsolete and should be ported."

# Standard Modules
from datetime import datetime

# Third Party Modules
import numpy as np
from numpy import exp, sqrt
import matplotlib.pyplot as plot

# Included Modules
from constants import *     # Useful elementary constants
import distributions        # Module containing various distributions
import rate                 # Determines reaction rates
import solver               # Handles general state calculations
import inout                # Input/output handling

#  Physical system options (user-defined)
T = 0.3e-6                           # duration to simulate, s
Te = 1.0 * q                         # effective electron temperature, J
ne = 1e10 * 1e6                      # background electron density, 1/m^3
Tg = 300                             # neutral gas temperature, K
P = 10.0 * 133.322                   # gas pressure, Pa
Ng = Na * 8.314 * Tg/P               # gas number density, 1/m^3
t0 = 0.0                             # initial time point, s
from gases import helium as gas      # choose gas to simulate
dist = distributions.drumax(0.5, Te) # load EEDF

# Pumping laser options, includes Doppler broadening, assumes perfect tuning
pump = False                # include laser pulse?
tau = 5e-9                  # pulsewidth, s
tl = 25e-9                  # time associated with the middle of the pulse, s
E = 10e-3                   # energy of the pulse, J
Alas = 1e-3 * 20e-3         # area of the beam focus spot, m^2
I0 = E/(Alas * tau)         # peak intensity, W/m^2
lstate = 210                # lower energy pump state
ustate = 311                # upper energy pump state

# Electron wave travelling through the observation area
wave = True 
dne = 1e12 * 1e6
tstart = 25e-9
ntau = 6e-13

# Solver options (user-defined)
hmin = 1e-22        # minimum time step, s
hmax = 1e-11        # maximum time step, s
TOL = 1.0e+15       # absolute allowable truncation error, 1/m^3

# Output options (user-defined)
dumprate = 0        # write data to disk after this many steps, 0 = never
prefix = 'wave'     # file prefix for data files

# Provide access to gas state information and matrix state order
states = gas.states.states
order = np.array(sorted(states.keys(), key=lambda state:states[state]['E']))

# Generate output wavelengths
#dim = len(order)
#wavelengths = np.zeros(sum(len(dim - 1))
#for i in range(dim - 1):
#    wavelengths[i*dim:(i + 1)*(dim - 1)] = states[order[i]]['E']

# Generate steady state transition matrices
Ae, Ao, Aa = solver.matrixgen(gas, dist, Te)
Arad = np.fill_diagonal(Ao.copy(), 0)

# Open data files for dump, check for pre-existing data, initialize arrays
fids, restart = inout.detect(prefix)
if restart:
    N, t0, eps = inout.load(fids)
else:
    eps = 0.0
    N = solver.equilibrium(Ae*ne + Ao + Aa*Ng) * Ng
populations = [N]
times = [t0]
errors = [eps]
emissions = []

# Generate supporting variables for laser pumping
if pump:
    il, iu = np.where(order == lstate), np.where(order == ustate)
    Anom = Ao[il, iu]
    Au = Ao[iu, iu]
    Al = Ao[il, il]
    gl, gu = states[lstate]['g'], states[ustate]['g']
    El, Eu = states[lstate]['E'], states[ustate]['E']
    nu = (Eu - El)/h
    L = h * c / (Eu - El)

# Define rate equation
def f(t, y):
    if wave:
        nmod = ne + (dne * exp(-(t - tstart)**2 / ntau**2))
        return np.dot((Ae*nmod + Ao + Aa*Ng), y)
    # Include any time dependent perturbations here
    if pump:
        I = I0 * exp(-(t - tl)**2 / tau**2)
        Aeff = Anom * L**3/(8*pi) * sqrt(gas.M / (8*pi*kB*Tg)) * I/(Eu - El)
        Ao[il, iu] = (Anom + Aeff)
        Ao[iu, iu] = Au - Ao[il, iu]
        Ao[iu, il] = (gu/gl) * Aeff
        Ao[il, il] = Al - Ao[iu, il]
    rates = np.dot((Ae*ne + Ao + Aa*Ng), y)
    return rates

def rad(A, N):
    pass
    

# Initialize solver and evolve states over time
stepper = solver.rkf45(f, times[0], populations[0], hmax, hmin, TOL)
start = datetime.now()
while times[-1] < T:
    N, t, eps = stepper.next()  # Step to next value with generator function
    emissions.append(rad(Arad, N))
    populations.append(N)
    times.append(t)
    errors.append(eps)

    # Output some useful information every 1000 steps
    if len(times)%1000 == 0:
        end = datetime.now()
        print "%g steps" % len(times)
        print "Real time:", times[-1]
        print "Simulation Time:", (end - start), "\n"

    # Dump output to external file at user-defined rate
    try:
        dump = bool(not len(times)%dumprate)
    except ZeroDivisionError:
        pass
    else:
        if dump:
            inout.save(fids, times, populations, errors)

populations = np.array(populations)
if restart:
    inout.save(fids, times[1:], populations[1:, :], errors[1:])
else:
    inout.save(fids, times, populations, errors)
