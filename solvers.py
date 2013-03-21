"""
Sets up the matrix and calculates the solutions.
"""

from constants import *

import numpy as np

def svd(matrix):
    """
    Determines the solution for a homogeneous system of equations in
    the for Ax = 0. The user supplies a matrix, A, as the input and
    the solution is found using the singular value decomposition
    method.
    """
    u, s, v = np.linalg.svd(matrix)
    #TODO: Is the last row of v always associated with the lowest s?
    null = np.abs(v[-1,:]).T
    return null

def dE(states, order):
    dim = len(states)
    mat = np.zeros((dim, dim))
    for i in range(dim):
        Ei = states[order[i]]['E']
        for f in range(dim):
            Ef = states[order[f]]['E']
            mat[i, f] = Ef - Ei
    return mat

def wavelengths(states, order):
    w = np.array([])
    for i in order:
        Ei = states[i]['E']
        for f in [j for j in order if j != i]:
            Ef = states[f]['E']
            if Ef < Ei:
                continue
            w = np.append(w, (h * c) / (Ef - Ei))
    return w

# ODE Solvers
# These are a selection of different solvers. 
# 

def rk4(f, x, y, h):
    # Simple fourth-order Runge-Kutta solver.
    k1 = h * f(x, y)
    k2 = h * f(x + 0.5*h, y + 0.5*k1)
    k3 = h * f(x + 0.5*h, y + 0.5*k2)
    k4 = h * f(x + h, y + k3)
    return y + k1/6 + k2/3 + k3/3 + k4/6

def rkf45(f, t0, y0, hmax, hmin, TOL, fixed=False):
    """
    Runge-Kutta-Fehlberg generator implemented per B. Bradie's "A
    Friendly Introduction to Numerical Analysis," incorporating
    automatic step control. Initialized by assigning the function to a
    variable which outputs the next step every time the .next() method
    is called.
    """

    A = [0.25,    0.25]
    B = [3./8,    3./32,       9./32]
    C = [12./13,  1932./2197, -7200./2197,   7296./2197]
    D = [1.0,     439./216,   -8.0,          3680./513,  -845./4104]
    E = [0.5,    -8./27,       2.0,         -3544./2565,  1859./4104, -11./40]
    F = [1./360, -128./4275,  -2197./75240,  1./50,       2./55]

    def k(f, t, y, h):
        k1 = h * f(t, y)
        k2 = h * f(t + A[0]*h, y + A[1]*k1)
        k3 = h * f(t + B[0]*h, y + B[1]*k1 + B[2]*k2)
        k4 = h * f(t + C[0]*h, y + C[1]*k1 + C[2]*k2 + C[3]*k3)
        k5 = h * f(t + D[0]*h, y + D[1]*k1 + D[2]*k2 + D[3]*k3 + D[4]*k4)
        k6 = h * f(t + E[0]*h, y + E[1]*k1 + E[2]*k2 + E[3]*k3 + E[4]*k4
                                 + E[5]*k5)
        errors = (F[0]*k1 + F[1]*k3 + F[2]*k4 + F[3]*k5 + F[4]*k6) / h
        return k1, k2, k3, k4, k5, k6, errors

    h = hmax
    y = y0
    t = t0

    while True:
        k1, k2, k3, k4, k5, k6, errors = k(f, t, y, h)
        rerrors = errors/y
        eps = np.max(abs(rerrors))

        if eps < TOL:
            y = y + (16./135)*k1 + (6656./12825)*k3 + (28561./56430)*k4 \
                  - (9./50)*k5 + (2./55)*k6
            t += h
            yield y, h, eps

        q = 0.84 * (TOL/eps)**0.25
        q = min(4.0, max(q, 0.1))
        h = min(q * h, hmax)

        if h < hmin:
            print "Warning, required step size is below minimum (h = %e)." % h
            raw_input('')
