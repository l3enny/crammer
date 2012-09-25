import numpy as np
from datetime import datetime

a = np.zeros((10, 1))
b = np.zeros((10, 1))
c = np.zeros(10)
l = [c]

t0 = datetime.now()
for i in range(5):
    a = np.append(a, b, axis=1)
    t1 = datetime.now()
    l.append(c)
    t2 = datetime.now()
    print "Method 1:", (t1 - t0)
    print "Method 2:", (t2 - t1)

convert = np.array(l)


print "a:\n", a
print "convert:\n", convert
