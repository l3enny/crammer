import csv
from scipy.constants import e, k
from numpy import loadtxt
from matplotlib import pyplot as plt

def emissions(times, intensities, wavelengths, step=1):
    I = loadtxt(intensities, delimiter=',')
    L = loadtxt(wavelengths, delimiter='\n')
    t = loadtxt(times, delimiter=',')
    select = [4, 7, 13, 16]
    visible = [10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
            28, 29, 30, 31]
    picks = visible
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
    plt.semilogy(1e9 * t[::step], k * Te[::step] / e, linewidth=2)
    plt.xlabel('Time (ns)')
    plt.ylabel('Electron Temperature (eV)')
    plt.savefig("temperatures.pdf")
    plt.clf()

if __name__ == "__main__":
    pre = '1torr'
    emissions(pre + "_times.csv", pre + "_emissions.csv", pre +
            "_wavelengths.csv")
    temperatures(pre + "_times.csv", pre + "_temperatures.csv")
    states(pre + "_times.csv", pre + "_populations.csv", pre +
            "_order.csv")
