"""
Main script for the energy-conserving CRM simulation, or global model.
The code should be pretty clear in its implementation, allowing the user
some flexibility in how the problem is solved.
"""

# User-specified settings
from species import *
from reactions import *
from settings import *

# Standard modules
from datetime import datetime

# Third party modules
import numpy as N

# Included modules
from constants import *    # physical constants
import distributions       # module containing different energy distributions
import handler             # handles input/output, interpreting data
import rate                # determines reaction rates
import solvers             # general solver module

