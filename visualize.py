from numpy import *
from matplotlib.pyplot import *

every = 10
target = 'dump'

populations = loadtxt(target + '_N.csv', delimiter=',')
times = loadtxt(target + '_t.csv', delimiter=',')

ion()
for state in range(populations.shape[1]):
    semilogy(times[::every], populations[::every, state])

ylabel('Populations (m$^{-3}$)')
xlabel('Time (s)')
raw_input('')
