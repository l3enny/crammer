"""
Basic load and save functions.
"""
import os
import numpy as np

def load(fids):
    params = []
    for fid in fids:
        old = fid.readlines()[-1].split(',')
        old[-1] = old[-1].strip('\n')
        params.append([float(i) for i in old])
    params[1] = np.array(params[1])
    return times, populations, errors, emissions
    
def save(fids, times, populations, errors, emissions):
    np.savetxt(fids[0], times, delimiter=',')
    np.savetxt(fids[1], populations, delimiter=',')
    np.savetxt(fids[2], errors, delimiter=',')
    #for i in emissions:
    #    print i
    #    raw_input('')
    np.savetxt(fids[3], emissions, delimiter=',')
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
