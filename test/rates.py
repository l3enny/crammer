from pylab import *

from constants import *
from gases import helium as gas
import rate
import distributions

istate = 100
fstate = 211

K1 = array([])

temperatures = logspace(-1, 2, num=1e3)*q
for temperature in temperatures:
    dist = distributions.drumax(1.0, temperature)
    transition = gas.electronic.Transition(istate, fstate)
    new = rate.rate(transition, dist)
    K1 = append(K1, new)

ion()
loglog(temperatures/q, K1*1e6, '--k')
xlabel('Electron Temperature, T$_\mathrm{e}$ (eV)')
ylabel('Rate coeff, K (cm$^3$/s)')
#axis([0.2, 90, 1.0e-6, 2.5e-4])
grid()
raw_input('')
