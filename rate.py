from numpy import array, log, exp, isnan, logspace, log10
from scipy.integrate import quad, trapz
from scipy.special import gamma

from constants import *

def rate(transition, f):
    if transition.undefined:
        return 0.0
    sigma = transition.sigma
    dE = transition.dE
    def integrand(E):
        # set up integrand for quadpack
        return sigma(E) * f(E) * (2*E/me)**0.5
    # Calculate the rate coefficient provided a list of electron temperatures
    # and the expected distribution
    if transition.inverse:
        Emin = -2
    else:
        Emin = log10(dE/q)
    Emax = log10((dE*1e3)/q)
    energies = logspace(Emin, Emax, num=1e4) * q
    values = integrand(energies)
    integral = trapz(values, energies)
    return integral
