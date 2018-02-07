#My (Artem Bolshakov) contributions

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as an
from scipy.interpolate import interp1d

def length(xs, ys):
    """
    Estimate of a curve's length.
    """
    xdeltas = np.array([xs[i] - xs[i - 1] for i in range(1, len(xs))])
    ydeltas = np.array([ys[i] - ys[i - 1] for i in range(1, len(xs))])
    return sum((xdeltas*xdeltas + ydeltas*ydeltas)**0.5)

"""
def prune(xs, ys, max=10):
    '''
    Only keep points within max of the origin.
    '''
    foundLower = False
    m = 0
    M = len(xs)
    for i in range(len(xs)):
        if (not foundLower):
            if xs[i]*xs[i] + ys[i]*ys[i] < max*max:
                foundLower = True
                m = i
                continue
        if foundLower:
            if xs[i]*xs[i] + ys[i]*ys[i] > max*max:
                M = i
                break
    print m
    print M
    print '\n'
    return xs[m:M], ys[m:M]
"""

def rescale(xs, ys, target=0.01):
    M = len(xs)
    L = length(xs, ys)
    
    #No need to LOSE resolution
    if L/target < M:
        return xs, ys

    #Parametrizing coordinate    
    coords = np.linspace(0, M-1, M)

    #Cubic spline interpolation functions
    csX = interp1d(coords, xs, kind='cubic')
    csY = interp1d(coords, ys, kind='cubic')

    #Denser points in parametrizing coordinate
    l = np.linspace(0, M-1, L/target)

    #New values
    newX = csX(l)
    newY = csY(l)

    return newX, newY


def active_region(vec, l):
    """
    Returns the portion that will exceed this vector in the next iteration.
    Only need to increment this part. Everything else is redundant.
    """
    M = len(vec)
    l = abs(l)
    if l < 1:
        return np.array(vec[int(math.floor(l*M)):M])
    else:
        return np.array(vec[int(math.floor(M/l)):M])













