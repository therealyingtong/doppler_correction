import numpy as np
import time
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import as_strided
import random
from scipy.linalg import toeplitz
import pycorrelate as pyc

arr1 = np.array(range(1,1001))
arr2a = np.array([])
arr2b = np.array(range(500,1001))
arr2 = np.concatenate((arr2a,arr2b))
lowerIdx = -1000
upperIdx = 0
numBins = 500
binSize = (upperIdx - lowerIdx) / numBins
bins = np.linspace(lowerIdx, upperIdx, numBins)
cc = pyc.pcorrelate(arr2,arr1,bins)

plt.figure()
plt.plot(bins[1:len(bins)], cc)
plt.show()

shift = (np.argmax(cc) - int(numBins / 2) ) * binSize
print('shift', shift)