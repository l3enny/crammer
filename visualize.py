import csv

from constants import *
from numpy import loadtxt
from matplotlib import pyplot as plt

def emissions(times, intensities, wavelengths, step=1):
    I = loadtxt(intensities, delimiter=',')
    L = loadtxt(wavelengths, delimiter=',')
    t = loadtxt(times, delimiter=',')
    select = [4, 7, 13, 16]
    nonzero = [0, 3, 4, 5, 6, 7, 8, 13, 19, 21, 22, 26, 31, 32, 35, 36, 38, 39,
            40, 42, 43, 45, 47, 49, 51, 53, 54, 58, 62, 70, 75, 76, 78, 79, 83,
            86, 87, 89, 94, 98, 101, 104, 105, 107, 109, 111, 112, 115, 117,
            128, 129, 134, 140, 144, 145, 151, 153, 155, 157, 159, 162, 163,
            165, 167, 168]
    visible = [13, 14, 15, 18, 19, 21, 24, 25, 26, 27, 31, 32, 33, 34, 39, 40,
            41, 42, 48, 49, 50, 51, 58, 59, 60, 61, 69, 70, 71, 72, 81, 82, 83,
            84, 94, 95, 96, 97, 108, 109, 110, 111, 123, 124, 125, 126, 139,
            140, 141, 156, 157, 158, 159, 175, 176, 177, 178, 179, 180, 181,
            182, 183]
    coincident = [i for i in visible if i in nonzero]
    picks = coincident
    plt.hold(True)
    for i in picks:
        plt.semilogy(1e9 * t[::step], I[::step,i], linewidth=2)
    labels = [int(round(i * 1e9, 0)) for i in L[picks]]
    plt.xlabel('Time (ns)')
    plt.ylabel('Intensity (a.u.)')
    plt.legend(labels)
    plt.savefig("emissions.pdf")
    plt.hold(False)
    plt.clf()

def states(times, states, labels, step=1):
    N = loadtxt(states, delimiter=',')
    t = loadtxt(times, delimiter=',')
    #select = range(N.shape[1])
    odd = [210, 310, 400, 201, 410, 312]
    tmeta = [210]
    with open(labels) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            l = row
    select = l
    indices = [l.index(str(i)) for i in select]
    plt.hold(True)
    for i in indices:
        plt.semilogy(1e9 * t[::step], N[::step, i], linewidth=3)
    #plt.axis((-350, 1650, 0, 5e16))
    plt.xlabel('Time (ns)')
    plt.ylabel('Density (1/m$^3$)')
    plt.legend(select)
    plt.savefig("populations.pdf")
    plt.hold(False)
    plt.clf()

def temperatures(times, temperatures, step=1):
    t = loadtxt(times, delimiter=',')
    Te = loadtxt(temperatures, delimiter=',')
    plt.semilogy(1e9 * t[::step], kB * Te[::step] / q, linewidth=2)
    plt.xlabel('Time (ns)')
    plt.ylabel('Electron Temperature (eV)')
    plt.savefig("temperatures.pdf")
    plt.clf()

if __name__ == "__main__":
    pre = 'dump'
    emissions(pre + "_times.csv", pre + "_emissions.csv", pre +
            "_wavelengths.csv")
    temperatures(pre + "_times.csv", pre + "_temperatures.csv")
    states(pre + "_times.csv", pre + "_populations.csv", pre +
            "_order.csv")
