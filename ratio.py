from gases import helium as gas
import rates

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import h, c, e, k

import cPickle


debug = False
num = 10000
temp1 = ([(310, 211), (300, 201)], "temperature_ratio1.csv")
temp2 = ([(410, 211), (402, 201)], "temperature_ratio2.csv")

transitions, saveas = temp2


#-----------------------------------------------------------------------------

states = gas.states.states

with open('./gases/helium/combined.pickle', mode='r') as f:
    coeffs = cPickle.load(f)

Ei = [states[transitions[0][0]]['E'], states[transitions[1][0]]['E']]
Ef = [states[transitions[0][1]]['E'], states[transitions[1][1]]['E']]

dE = [Ei[0] - Ef[0], Ei[1] - Ef[1]] 
l = [(h * c)/i for i in dE]

# calculate line-specific radiative transition rates
A = [gas.optical.A(transitions[0][0], transitions[0][1]),
     gas.optical.A(transitions[1][0], transitions[1][1])]

# calculate total radiative transition rates
Atot = [0.0, 0.0]
for s in states:
    Atot[0] += gas.optical.A(transitions[0][0], s)
    Atot[1] += gas.optical.A(transitions[1][0], s)

temperatures = np.logspace(-1, np.log10(200), num=num)
ratios = np.zeros(num)

for i in range(num):
    T = temperatures[i] * e / k

    # calculate rate coefficients
    X = [coeffs.rate(T, 100, transitions[0][0]), 
         coeffs.rate(T, 100, transitions[1][0])]
    X = [max(0.0, j) for j in X]

    if debug:
        print "l:", l
        print "A:", A
        print "Atot:", Atot
        print "X:", X
        raw_input('')

    # calculate line ratios
    try:
        ratios[i] = (l[1] * A[0]    * Atot[1] * X[0]) / \
                    (l[0] * Atot[0] * A[1]    * X[1])
    except ZeroDivisionError:
        ratios[i] = 0.0

output = np.zeros((num, 2))
output[:, 0] = temperatures
output[:, 1] = ratios

with open(saveas, mode="w") as f:
    f.write("Temperatures,%g->%g/%g->%g\n" % tuple([i for j in transitions for i
        in j]))
    np.savetxt(f, output, delimiter=",")
