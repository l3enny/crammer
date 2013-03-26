import numpy as np
from scipy.interpolate import UnivariateSpline
from constants import *

N0 = 2.688e19 * 1e6

Tsim = np.array([1.620e-1, 2.415e-1, 4.388e-1, 8.413e-1, 1.268e+0, 1.736e+0,
2.808e+0, 4.188e+0, 4.511e+0, 4.713e+0, 4.999e+0, 5.437e+0, 5.825e+0, 6.198e+0,
6.565e+0, 7.301e+0, 8.064e+0, 9.079e+0, 1.018e+1, 1.144e+1, 1.287e+1, 1.490e+1,
1.818e+1]) * q / kB

constants = [4.303e11, 5.370e11, 7.376e11, 1.020e12, 1.226e12, 1.391e12,
        1.639e12, 1.819e12, 1.845e12, 1.860e12, 1.879e12, 1.904e12, 1.922e12,
        1.936e12, 1.946e12, 1.957e12, 1.961e12, 1.958e12, 1.948e12, 1.931e12,
        1.908e12, 1.874e12, 1.825e12]

def K(Te):
    if all([Te > i for i in Tsim]):
        print("WARNING: Temperature above calculation boundary,"
              " extrapolating.")
    if all([Te < i for i in Tsim]):
        print("WARNING: Temperature below calculation boundary,"
              " extrapolating.")
    # Catch cases not covered by Kushner's simulation, and approximate
    # population of upper states so for emission tracking
    interp = UnivariateSpline(np.array(Tsim), constants, s=0)
    return interp(Te)
