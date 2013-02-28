"""
Basic load and save functions.
"""
import os
import numpy as N

def load_kushner(fid):
    for line in fid:
        if "RATE CONST" in line:
            
    return None

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

def detect(prefix):
    names = ['_t', '_N', '_e', '_l']
    names = [prefix + sub + '.csv' for sub in names]
    options = {'':'a', 'Y':'a', 'y':'a', 'yes':'a', 'Yes':'a', 'YES':'a',
               'N':'w', 'n':'w', 'no':'w', 'No':'w'}
    fids = []
    restart = False
    try:
        size = os.path.getsize(names[0])
    except OSError:
        mode = 'w'
        pass
    else:
        while True:
            choice = raw_input('File already exists, would you like to'
                               ' load the last time step? [Y/n]')
            try:
                mode = options[choice]
            except (KeyError, IndexError, TypeError):
                print "Invalid input, try again."
                continue
            else:
                break
    if mode is 'a':
        restart = True
    for name in names:
        fid = open(name, mode)
        fids.append(fid)
    return fids, restart
