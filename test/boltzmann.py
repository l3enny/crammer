from math import exp
from matplotlib import pyplot as plot
from gases import helium as gas

T = 1.0 * 1.6022e-19

states = gas.states.states
indices = sorted(states.keys(), key=lambda state:states[state]['E'])

populations = []
energies = []

for state in indices:
    if state == 100:
        populations.append(1.0)
    else:
        g = states[state]['g']
        E = states[state]['E']
        populations.append(g * exp(-E/T))
    energies.append(states[state]['E'])

plot.ion()
plot.semilogy(populations)
raw_input('')
