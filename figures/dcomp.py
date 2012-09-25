from constants import *
import distributions

import numpy as np
x = [0.5, 0.75, 1.0, 1.25, 1.50]
energies = np.logspace(-1, 2, num=1e2) * q

f = []
for i in x:
    d = distributions.drumax(i, q)
    calc = np.array(d(energies))
    f.append(calc)

np.savetxt('dcomp.csv', f, fmt='%e', delimiter=',')
