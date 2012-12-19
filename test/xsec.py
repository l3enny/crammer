from pylab import *

from constants import *
from gases import helium as gas
from numpy import logspace, array

t = gas.electronic.Transition(100, 210)
s1 = t.sigma

# Check that the single argument works
print "Cross section at 1eV:", s1(array([1.602e-19]))

# Plot 
energies = logspace(-1, 2, num=1e3)*q

loglog(energies/q, s1(energies)*1e4, '--k')
xlabel('Electron Energy (eV)')
ylabel('Cross-section, $\sigma$ (cm$^2$)')
grid()
show()
