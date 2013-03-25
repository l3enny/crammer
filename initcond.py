import solvers

def equilibrium(A):
    # Determines the equilibrium values for the populations based solely on
    # temperature. NB unless the electron density is subsequently set equal to
    # the ion density, this will likely result in deviation from neutrality.
    # Values are normalized to the gas density.
    err = 1.0
    TOL = 1.0e-6
    n = 1.0
    while err > TOL:
        N = solvers.svd(A)
        err = abs(n - N[-1]) / N[-1]
        n = N[-1]
        print "N =", N
    return N

