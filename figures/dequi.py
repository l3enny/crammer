from gases import helium
import solver
import distributions
from constants import *
import matplotlib.pyplot as plot
import numpy as np
from numpy import matrix

ne = 1.0e10 * 1.0e6
T = 1.0 * q
f = distributions.drumax(1.00, T)

Ae, Ao, Aa = solver.matrixgen(helium, f, T)
A = Ae*ne + Ao + Aa

x = solver.equilibrium(A)

np.savetxt('eq_1.00.csv', x, delimiter=',')
