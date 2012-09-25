"""
File containing various distribution functions for testing. These can
be imported and passed to the rate solver as desired. It should be
easy to add to this file. NOTE: All distribution functions must be
continuous! Yes, this is inconvenient, but (at the moment) the rate
calculations do not evaluate at predictable or specified values of E.
"""

from numpy import array, log, exp
from scipy.special import gamma

from constants import *

def drumax(x, T):
    def dist(E):
        # Maxwellian for x = 1, Druyvesteyn for x = 2
        c1 = x * (2.0/3.0)**1.5 * (gamma(2.5/x))**1.5 / (gamma(1.5/x))**2.5
        c2 = ((2.0/3.0) * gamma(2.5/x) / gamma(1.5/x))**x
        return c1 * T**-1.5 * E**0.5 * exp(-c2 * (E/T)**x)
    return dist

def maxwellian(T):
    def dist(E):
        return 2/pi**0.5 * T**-1.5 * E**0.5 * exp(-E/T)
    return dist
