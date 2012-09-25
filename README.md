# CRAMMER - Collisional RAdiative Model MER

## Introduction
Don't ask what the MER is for, I don't know.

This is a collisional radiative model for plasmas which can track
ionization and emission in a 0D simulation. The code uses a framework
approach, that is, you are mostly responsible for writing the simulation
(I just make it easier for you). The current version only supports
neutral helium (exiciting I know) and includes the cross section tables
of Ralchenko.

## Getting Started
Probably the best place to learn how the code works is in `script.py`.
This is a simple equilibrium simulation script and is commented
well-enough for someone who has some idea of what they're doing. Cross
sections are contained in `gases/` and there are some basic tests of the
underlying functions in `tests/`. That's about it for the moment.

## The FUTURE
I'm not entirely sure where I'm going with this. I'd like to add some
functionality to the framework to further automate the simulations. As
is, the basic script is longer than it should be. Likewise, the
simulation of a laser interacting with the plasma (found in `obsolete/`)
is a bit of a hack (I modify the transition matrices directly). There's
also some to be added to the physics. It would be nice to cover the
first ionized state of helium, but the cross sections don't really exist
for that. Other gases would be nice too. One thing I've neglected for a
while is including the excited-excited and excited-ground collisions.
The latter of which is quite possibly important. 
