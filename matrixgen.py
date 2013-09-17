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
    """
    Shim to the effective momentum transfer frequency from rate generator.
    """
    return gas.km.K(Te)

def electronic(gas, coeffs, Te):
    """
    Electron collision-induced transitions between states.
    """
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    mat = N.zeros((dim, dim))
    # Move down the rows, equivalent to rate equation for each final state
    for f in range(dim):
        # Move across the columns: access each upper initial state
        for i in range(dim):
            mat[f,i] = coeffs.rate(Te, order[i], order[f])
    for i in range(dim):
        mat[i, i] = -N.sum(mat[:, i])
    return mat

def atomic(gas):
    """
    Excitation transfer between states via ground-state collisions.
    """
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    mat = N.zeros((dim, dim))
    # Move down the rows, equivalent to rate equation for each final state
    for f in range(dim):
        # Move across the columns: access each upper initial state
        for i in range(dim):
            mat[f,i] = gas.atomic.K(order[i], order[f])
    for i in range(dim):
        mat[i, i] = -N.sum(mat[:, i])
    return mat

def optical(gas):
    """
    Generates array of radiative transition rates.
    """
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    mat = N.zeros((dim, dim))
    for i in range(1, dim):
        for f in range(i):
            mat[f, i] = gas.optical.A(order[i], order[f])
        mat[i, i] = -sum(mat[:, i])
    return mat

def g_ratio(gas):
    """
    Generates array of statistical degeneracies
    """
    states = gas.states.states
    order = sorted(states.keys(), key=lambda state:states[state]['E'])
    dim = len(states)
    mat = N.zeros((dim, dim))
    for i in range(1, dim):
        g_i = states[order[i]]['g']
        for f in range(i):
            g_f = states[order[f]]['g']
            mat[f, i] = g_f / g_i
        mat[i, i] = 1.0
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
