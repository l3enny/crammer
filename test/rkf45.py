import solver
import numpy as np
import matplotlib.pyplot as plot

plot.ion()

initt = 0.0
initx = 0.0
hmin = 0.01
hmax = 0.25
TOL = 5e-7
T = 5

times = np.array([initt])
solutions = [initx]
errors = [0.0]

def f(t, x):
    return -3*t*x**2 + 1/(1 + t**3)

stepper = solver.rkf45(f, initt, initx, hmax, hmin, TOL)
while times[-1] < T:
    new, t, eps = stepper.next()
    solutions.append(new)
    times = np.append(times, t)
    errors.append(eps)

plot.plot(times, solutions)
raw_input('')
