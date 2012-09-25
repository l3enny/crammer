import numpy as np
from constants import q
from matplotlib.pyplot import *
import distributions
from numpy import exp

Te = 8.7 * q

d1 = distributions.drumax(0.5, Te)
d2 = distributions.starikovskaia(Te)

E = np.linspace(0, 100, num=1e3) * q

f1 = d1(E)
f2 = d2(E)

ion()
semilogy(E/q, f1, '-k')
semilogy(E/q, f2, '--k')
ylabel('EEDF, eV$^{-3/2}$')
xlabel('Electron Energy, eV')
raw_input('')
