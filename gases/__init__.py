"""
Subpackage which defines all the transition constants for the named gas.
At present there is only one gas module, helium. If any gases are added,
they should follow its example in being self-contained. All methods for
calculating cross sections should be transparent to the main program.
In the future, I need to come up with a spec for gas packages.
"""

__all__ = ['helium']
