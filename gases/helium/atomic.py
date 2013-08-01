"""These are atomic excitation transfer rate coefficients from 
Dubreuil and Catherinot.
"""

from constants import M
from scipy.constants import k
from math import sqrt

A2 = (1e-10)**2
v_th = sqrt(k * 300 / M)
Q = {
        302:{301:10e-20},
        301:{302:27e-20},
        311:{312:0.15e-20},
        312:{311:1.2e-20},
        402:{401:10e-20,   400:3.5e-20,  403:9.25e-20, 413:9.25e-20},
        401:{402:21e-20},
        400:{402:3.0e-20,  403:0.9e-20,  413:0.9e-20},
        403:{402:2.35e-20, 400:0.5e-20,  412:1.75e-20, 411:1.0e-20, 410:0.5e-20},
        413:{402:2.35e-20, 400:0.5e-20,  412:1.75e-20, 411:1.0e-20, 410:0.5e-20},
        412:{403:3.3e-20,  413:3.3e-20,  411:8.8e-20,  410:3.5e-20},
        411:{403:1.5e-20,  413:1.5e-20,  412:5.8e-20,  410:2.9e-20},
        410:{403:0.05e-20, 413:0.05e-20, 412:0.7e-20,  411:0.3e-20},
        }

def K(istate, fstate):
    try:
        sigma = Q[istate][fstate]
    except KeyError:
        sigma = 0.0
    rate = v_th * sigma
    return rate

def test():
    print M
