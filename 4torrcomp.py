import csv

from constants import *
from numpy import loadtxt, linspace
from matplotlib import pyplot as plt

def states(times, states, labels, step=1):
    N = loadtxt(states, delimiter=',')
    t = loadtxt(times, delimiter=',')
    meas = loadtxt('4torrfits.csv', delimiter=',')
    tmeas = linspace(0, 2000, 5e3)
    nmeas = meas[:,1]/0.033
    odd = [210, 310, 400, 201, 410, 312]
    tmeta = [210]
    select = tmeta
    with open(labels) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            l = row
    indices = [l.index(str(i)) for i in select]
    plt.hold(True)
    plt.plot(tmeas-328, nmeas, '-r', linewidth=3)
    for i in indices:
        plt.plot(1e9 * t[::step], N[::step, i], linewidth=3)
    plt.axis((0, 170, 0, 5e17))
    plt.xlabel('Time (ns)')
    plt.ylabel('Density (1/m$^3$)')
    plt.legend(('Measured', 'Simulated'))
    plt.savefig("4torrpopulations.pdf")
    plt.hold(False)
    plt.clf()

if __name__ == "__main__":
    pre = 'dump'
    states(pre + "_times.csv", pre + "_populations.csv", pre +
            "_order.csv")
