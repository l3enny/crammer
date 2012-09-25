from constants import q, amu
import electronic, optical, atomic  # these modules do all the work, this file
                                    # is just a wrapper for their internal
                                    # functions.

M = 4.002602 * amu

# *generates and returns* a cross section function
def sigma_e(istate, fstate):
    return electronic.sigmagen(istate, fstate)

def A(istate, fstate):
    return optical.A(istate, fstate)

def K(istate, fstate):
    return atomic.K(istate, fstate)

