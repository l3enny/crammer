from gases import helium
from constants import *
import distributions
import rate

import numpy as np
from matplotlib.pyplot import *

ion()

istate = 311
#fstate = 310
#fstate = 412
fstate = 412

target = str(istate) + '_to_' + str(fstate) + '.csv'

transition = helium.electronic.Transition(istate, fstate)

x = [0.5, 0.75, 1.0, 1.25, 1.50]
rates = []
temperatures = np.logspace(-1, 2, num=1e2) * q

for i in x:
    K = []
    for T in temperatures:
        d = distributions.drumax(i, T)
        K.append(rate.rate(transition, d))
    rates.append(K)

np.savetxt(target, rates, fmt='%e', delimiter=',')
