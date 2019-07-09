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

def pad(arr1, arr2):
    if len(arr1)> len(arr2):
        for i in range(len(arr1)-len(arr2)):
            arr2.append(0)
    else:
        for i in range(len(arr2)-len(arr1)):
            arr1.append(0)
            
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
    
    print('shift',shift)
    # plt.plot(c)
    # plt.show()

    return shift