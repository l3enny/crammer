"""
Definitions of convenient constants. Do not change these unless the laws of the
universe change.
"""

from math import pi, e

# Defined/measure cosntants
c = 2.99792458e8        # m/s, exact
q = 1.60217646e-19      # C
amu = 1.660538921e-27   # kg
me = 9.10938291e-31     # kg
mu0 = 4e-7 * pi         # V.s/(A.m), exact
h = 6.62606957e-34      # J.s
kB = 1.3806488e-23      # J/K
Na = 6.02214129e23      # Avogadro number

# Derived Constants
ep0 = 1 / (c**2 * mu0)                  # F/m, exact
hbar = h/(2*pi)                         # J.s
a0 = 4*pi*ep0*hbar**2/(me*q**2)         # Bohr radius, m
Rinf = me*q**4/(8 * ep0**2 * h**3 * c)  # 1/m
Ry = h * c * Rinf                       # J
