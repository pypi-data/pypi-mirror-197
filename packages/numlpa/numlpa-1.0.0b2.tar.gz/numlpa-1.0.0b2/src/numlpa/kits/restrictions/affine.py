# -*- coding: utf-8 -*-

"""Affine restriction.

This module restricts the interval of the variable to the part where
the transformed amplitude is affine.

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
