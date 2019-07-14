import numpy as np
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt

import random
from scipy.linalg import toeplitz

import pyximport; pyximport.install()

def timebin(arr,t):
    counter =0
    binnedArray = [0]

    i = 0
    while i < (len(arr)):
        if arr[i]>=counter*t:
            counter += 1
            binnedArray.append(0)
            continue
        i+=1
        binnedArray[-1]+=1
    
    return list(np.array(binnedArray))

def firstZeroIndex(arr):
    for i in range(len(arr)):
        print(arr[i])
        if arr[i] == 0:
            return i

def sortArrLen(arr1, arr2):
    # return arrays ordered in ascending order of array length
    if len(arr1) > len(arr2):
        return arr2, arr1
    else:
        return arr1, arr2

def findMinOfTwoArrays(arr1, arr2):
    return min([min(arr1), min(arr2)])

def pad(arr1, arr2):

    diffLen = abs(len(arr1) - len(arr2))
    pad = np.zeros(diffLen)

    if len(arr1)> len(arr2):
        arr1 = np.concatenate([arr1, np.zeros(len(arr1))])
        arr2 = np.concatenate([arr2, np.zeros(len(arr2)), pad, pad])

    else:
        arr2 = np.concatenate([arr2, np.zeros(len(arr2))])
        arr1 = np.concatenate([arr1, np.zeros(len(arr1)), pad, pad])

    return arr1, arr2

def cross_correlation_using_fft(x, y):
    f1 = fft(x)
    f2 = fft(np.flipud(y))
    cc = np.real(ifft(f1 * f2))
    return fftshift(cc)

def compute_shift(x, y):
    assert len(x) == len(y)
    c = cross_correlation_using_fft(x, y)

    assert len(c) == len(x)
    zero_index = int(len(x) / 2) - 1
    shift = zero_index - np.argmax(c)
    
    # plt.plot(c)
    # plt.show()

    return shift