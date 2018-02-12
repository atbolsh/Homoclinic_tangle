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


def prune(xs, ys, m=10):
    '''
    Only keep points within max of the origin.
    '''
    indeces = range(len(xs))
    newXs = np.asarray([xs[i] for i in indeces if xs[i]< m and ys[i] < m])
    newYs = np.asarray([ys[i] for i in indeces if ys[i]< m and xs[i] < m])
    return newXs, newYs


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













