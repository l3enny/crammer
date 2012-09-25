from gases import helium as gas
import numpy as np

istate = 100
fstate = 201
E = np.array([1.6022e-19, 1.6022e-18, 1.6022e-17])

t = gas.electronic.Transition(istate, fstate)
sigma = t.sigma

print "t.dE =", t.dE
print "s =", sigma(E)
