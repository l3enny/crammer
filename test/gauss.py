import gel
import numpy as np

A = np.array([[1, 1, 1, 1], [1, 1, 2, 3], [-1, 0, 2, 1], [3, 2, -1, 0]])
b = np.array([[1], [2], [1], [1]])

x = gel.solve(A, b)

print x
