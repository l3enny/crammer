"""
Basic load and save functions.
"""
import os
import re

import numpy as N

def save(data, prefix='dump'):
    # responsible for saving all the passed variables
    names = ['times', 'populations', 'errors', 'emissions', 'wavelengths']
    if len(names) != len(data):
        raise ValueError('Insufficient output data')
    for i in range(len(names)):
        with open(prefix + '_' + names[i] + '.csv', 'w') as fid:
            N.savetxt(fid, data[i], delimiter=',')
    return None

def loadkushner(path):
    # This is a really hacky way of parsing Kushner's rate coefficient file. It
    # is fragile and does not like change.
    E = []
    with open(path) as fid:
        for line in fid.readlines():
            # Check if the line marks a new case
            if '*****' in line:
                
        pass
