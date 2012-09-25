from pylab import *

from constants import *
from gases import helium as gas
import rate
import distributions

istate = 311
fstate = 310

states = gas.states.states

K1 = array([])
K2 = array([])

temperatures = logspace(-1, 2, num=1e3)*q
for temperature in temperatures:
    dist = distributions.drumax(1.0, temperature)
    
    # Calculate using inverse cross sections
    t1 = gas.electronic.Transition(istate, fstate)
    n1 = rate.rate(t1, dist)
    K1 = append(K1, n1)

    # Calculate using inverse rate
    Ei = states[istate]['E']
    Ef = states[fstate]['E']
    gi = states[istate]['g']
    gf = states[fstate]['g']
    t2 = gas.electronic.Transition(fstate, istate)
    n2 = rate.rate(t2, dist)
    in2 = n2 * (gf/gi) * exp((Ei-Ef)/temperature)
    K2 = append(K2, in2)


ion()
loglog(temperatures/q, K1*1e6, '--k')
loglog(temperatures/q, K2*1e6, '-k')
xlabel('Electron Temperature, T$_\mathrm{e}$ (eV)')
ylabel('Rate coeff, K (cm$^3$/s)')
legend(['Inverse Cross Section', 'Inverse Rate'])
grid()
axis([0.2, 90, 1e-6, 2.5e-4])
raw_input('')

clf()
plot(K2/K1)
raw_input('')
