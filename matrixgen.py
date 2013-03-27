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
    return gas.km.K(Te)

#def electronic(gas, Te):
#    states = gas.states.states
#    order = sorted(states.keys(), key=lambda state:states[state]['E'])
#    dim = len(states)
#    mat = N.zeros((dim, dim))
#    for i in range(dim):
#        for f in range(i+1, dim):
#            mat[f, i], mat[i, f] = gas.electronic.rates(Te, order[i], order[f])
#        mat[i, i] = -N.sum(mat[:, i])
#    return mat

def electronic(gas, Te):
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    mat = N.zeros((dim, dim))
    # Move down the rows, equivalent to rate equation for each final state
    for f in range(dim):
        # Move across the columns: access each upper initial state
        for i in range(dim):
            mat[f,i] = gas.electronic.rates(Te, order[i], order[f])
    for i in range(dim):
        mat[i, i] = -N.sum(mat[:, i])
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

def linopt(gas):
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    lin = []
    for f in range(dim):
        for i in range(f):
            lin.append(gas.optical.A(order[f], order[i]))
    return N.array(lin)

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
