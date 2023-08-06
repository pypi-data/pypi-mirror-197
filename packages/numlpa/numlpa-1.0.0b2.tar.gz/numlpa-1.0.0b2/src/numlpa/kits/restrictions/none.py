# -*- coding: utf-8 -*-

"""No restriction.

This module does not apply any restriction on the variable interval
for model fitting.

"""


def limit(variable, amplitude):
    """Return the index of the last value to consider.

    Parameters
    ----------
    variable : list of float
        Fourier variable values.
    amplitudes : list of float
        Fourier transform amplitudes.

    Returns
    -------
    int
        Index of the last Fourier variable to be considered.

    """
    _ = amplitude
    return len(variable)
