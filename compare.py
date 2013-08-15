import csv
import os

from constants import *
from numpy import loadtxt, linspace, average
from matplotlib import pyplot as plt

if __name__ == "__main__":
    pre = '1torr'
    triplet_metastable = ['210']
    select = triplet_metastable
    length = 3.3 * 1e-2 # pathlength of integrated data
    step = 1        # reduce data density by this amount
    delay = 282     # negative shift for measured data in ns
    initial = 0.0   # baseline shift for calculated data
    zero_correct = True # correct for small offset in measurements

    indices = []
    with open(pre + '_order.csv') as csvfile:
        line = csv.reader(csvfile, delimiter=',').next()
        for s in select:
            indices.append(line.index(s))

    # Read in data
    N = []
    t = []
    N = loadtxt(pre + '_populations.csv', delimiter=',')
    t = loadtxt(pre + '_times.csv', delimiter=',')
    Navg_meas = loadtxt('fitparams.csv', delimiter=',', skiprows=1)[:, 2]
    N_meas = Navg_meas/length
    t_meas = linspace(0, 2e3, 5e3) * 1e-9
    if zero_correct:
        shift = average(N_meas[:200])
        N_meas = N_meas - shift

    labels = ['Measured', 'Simulated']
    plt.plot((1e9 * t_meas), N_meas)
    plt.hold(True)
    for j in indices:
        plt.plot(1e9 * t[::step] + delay, N[::step, j] + initial)
    plt.axis((286, 456, 0, 2e17))
    plt.xlabel('Time (ns)')
    plt.ylabel('Density (1/m$^3$)')
    plt.legend(labels , loc=4)
    #plt.savefig("compare.pdf")
    plt.show()
