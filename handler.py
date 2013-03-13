"""
Basic load and save functions.
"""
import os
import numpy as N

def save(prefix, data):
    # responsible for saving all the passed variables
    names = ['times', 'populations', 'errors', 'emissions', 'wavelengths']
    if len(names) != len(data):
        raise ValueError('Insufficient output data')
    for i in range(len(names)):
        fid = open(prefix + '_' + names[i] + '.csv', 'w')
        N.savetxt(fid, data[i], delimiter=',')
        fid.close()
    return None

