"""
Basic load and save functions.
"""
import os
import numpy as N

def load(fids):
    params = []
    for fid in fids:
        old = fid.readlines()[-1].split(',')
        old[-1] = old[-1].strip('\n')
        params.append([float(i) for i in old])
    params[1] = N.array(params[1])
    return times, populations, errors, emissions
    
def save(fids, times, populations, errors, emissions):
    N.savetxt(fids[0], times, delimiter=',')
    N.savetxt(fids[1], populations, delimiter=',')
    N.savetxt(fids[2], errors, delimiter=',')
    N.savetxt(fids[3], emissions, delimiter=',')
    return None

def close(fids):
    for fid in fids:
        fid.close()
    return None
