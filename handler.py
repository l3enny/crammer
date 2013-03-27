"""
Basic load and save functions.
"""
import os
import re

import numpy as N

def save(data, names, prefix='dump'):
    print "Saving data to disk ...\n"
    # responsible for saving all the passed variables
    if len(names) != len(data):
        raise ValueError('Insufficient output data')
    for i in range(len(names)):
        with open(prefix + '_' + names[i] + '.csv', 'w') as fid:
            N.savetxt(fid, data[i], delimiter=',')
    return None
