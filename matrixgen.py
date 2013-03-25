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

def km(gas, Te):
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    km = []
    for i in range(dim):
        km.append(gas.electronic.rates(Te, order[i], 'elastic')[0])
    return sum(km)

def electronic(gas, Te):
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    mat = N.zeros((dim, dim))
    for i in range(dim):
        for f in range(i+1, dim):
            mat[i, f], mat[f, i] = gas.electronic.rates(Te, order[i], order[f])
        mat[i, i] = -N.sum(mat[i, :])
    return mat

def optical(gas):
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    mat = N.zeros((dim, dim))
    for i in range(1, dim):
        for j in range(i):
            mat[j, i] = gas.optical.A(order[i], order[j])
        mat[i, i] = -sum(mat[:, i])
    return mat

def atomic(gas):
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    mat = N.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            mat[j, i] = gas.atomic.K(order[i], order[j])
        mat[i, i] = -sum(mat[:, i])
    return mat
