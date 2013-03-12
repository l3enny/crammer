"""
Basic load and save functions.
"""
import os
import numpy as N

def open():
    # function that opens the necessary files and returns their ids
    pass

def save(times, populations, errors, emissions):
    # responsible for saving all the passed variables
    fids = open()
    N.savetxt(fids[0], times, delimiter=',')
    N.savetxt(fids[1], populations, delimiter=',')
    N.savetxt(fids[2], errors, delimiter=',')
    N.savetxt(fids[3], emissions, delimiter=',')
    return None

def close(fids):
    # closes all files opened for writing out the results
    for fid in fids:
        fid.close()
    return None
