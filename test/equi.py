"""
Check to ensure that the SVD solver properly determines the null space,
ie, the solution to the homogeneous system of equations. 
"""

from gases import helium
import solvers
import distributions
from constants import *
import numpy as np

ne = 1.0e02 * 1.0e6
T = 1.0 * q
f = distributions.drumax(0.50, T)
eps = 1e-6

states = helium.states.states
order = np.array(sorted(states.keys(), key=lambda state:states[state]['E']))

Ae, Ao, Aa = solvers.matrixgen(helium, f, T)
A = lambda n: Ae*n + Ao + Aa

err = 1.0
while err > eps:
    x = solvers.equilibrium(A(ne)) * 1.49e22
    err = abs(ne - x[-1])/x[-1]
    ne = x[-1]
    print 'ne =', ne

print 'Order:', order
print 'x =', x
