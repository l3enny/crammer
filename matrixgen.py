"""
Generates the electronic, optical and atomic transition matrices
for a specified gas module. A functional EEDF, f, must be supplied
which takes the energy as its only argument. The matrices are
populated in an "intelligent" order such that the total population
is preserved and de-excitation rates are calculated via the
principle of detailed balance.
"""

import numpy as N

import rate

states = gas.states.states
order = sorted(states.keys(), key=lambda state:states[state]['E'])
dim = len(states)



def electronic(gas, f, Te):
    mat = N.zeros((dim, dim))
    for in in range(dim):
        gi = states[order[i]]['g']
        Ei = states[order[i]]['E']
        for j in range(i + 1, dim):
            gf = states[order[j]]['g']
            Ef = states[order[j]]['E']
            transition = gas.electronic.Transition(order[i], order[j])
            down = rate.rate(transition, f)
            mat[j, i] = down
            mat[i, j] = down * (gf/gi) * N.exp((Ei - Ef)/Te)
        mat[i, i] = -sum(mat[:,i])
    return mat

def optical(gas):
    mat = N.zeros((dim, dim))
    for i in range(1, dim):
        for j in range(i):
            mat[j, i] = gas.optical.A(order[i], order[j])
        mat[i, i] = -sum(mat[:, i])
    return mat

def atomic(gas):
    mat = N.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            mat[j, i] = gas.atomic.K(order[i], order[j])
        mat[i, i] = -sum(mat[:, i])
        return mat

