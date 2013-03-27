import csv

from constants import *
from numpy import loadtxt
from matplotlib import pyplot as plt

def emissions(times, intensities, wavelengths, step=1):
    I = loadtxt(intensities, delimiter=',')
    L = loadtxt(wavelengths, delimiter=',')
    t = loadtxt(times, delimiter=',')
    select = [4, 7, 13, 16]
    nonzero = [0, 3, 4, 5, 6, 7, 8, 13, 15, 16, 20]
    plt.hold(True)
    for i in select:
        plt.plot(1e6 * t[::step], I[::step,i], linewidth=2)
    labels = [int(round(i * 1e9, 0)) for i in L[select]]
    plt.xlabel('Time ($\mu$s)')
    plt.ylabel('Intensity (a.u.)')
    plt.legend(labels)
    plt.savefig("emissions.pdf")
    plt.hold(False)

def states(times, states, labels, step=1):
    N = loadtxt(states, delimiter=',')
    t = loadtxt(times, delimiter=',')
    with open(labels) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            l = row
    plt.hold(True)
    for i in range(N.shape[1]):
        print "Iteration", i
        print N[::step, i]
        print "Label:", l[i]
        raw_input('')
        plt.plot(1e6 * t[::step], N[::step, i], linewidth=2)
    plt.xlabel('Time ($\mu$s)')
    plt.ylabel('Density (1/m$^3$)')
    plt.legend(l)
    plt.savefig("populations.pdf")
    plt.hold(False)

def temperatures(times, temperatures, step=1):
    t = loadtxt(times, delimiter=',')
    Te = loadtxt(temperatures, delimiter=',')
    plt.semilogy(1e6 * t[::step], kB * Te[::step] / q, linewidth=2)
    plt.xlabel('Time ($\mu$s)')
    plt.ylabel('Electron Temperature (eV)')
    plt.savefig("temperatures.pdf")

if __name__ == "__main__":
    pre = 'dump'
    emissions(pre + "_times.csv", pre + "_emissions.csv", pre +
            "_wavelengths.csv")
    temperatures(pre + "_times.csv", pre + "_temperatures.csv")
    states(pre + "_times.csv", pre + "_populations.csv", pre +
            "_order.csv")
