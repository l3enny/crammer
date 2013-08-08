import numpy as np
from scipy.constants import e
from gases import helium as gas
import rate
import distributions

istate = 100
fstate = 'ion'

K1 = np.array([])

temperatures = np.logspace(-1, 1.5, num=1e2) * e
for temperature in temperatures:
    dist = distributions.drumax(1.0, temperature)
    transition = gas.electronic.Transition(istate, fstate)
    new = rate.rate(transition, dist)
    K1 = np.append(K1, new)

np.save("ion_rates.npy", K1)

#loglog(temperatures/q, K1*1e6, '--k')
#xlabel('Electron Temperature, T$_\mathrm{e}$ (eV)')
#ylabel('Rate coeff, K (cm$^3$/s)')
##axis([0.2, 90, 1.0e-6, 2.5e-4])
#grid()
#show()

#savetxt("ion_rates.csv", K1, delimiter=',')
#savetxt("temps.csv", temperatures, delimiter=",")
