# parse binary data

#import dataGenerator
import helper
import numpy as np
import time
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt

import random
from scipy.linalg import toeplitz

import pyximport; pyximport.install()

import sys

filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]

def parseStamp(filename):
    openedFile = open(filename, 'rb')
    stamp = np.fromfile(file=openedFile, dtype='<u4').reshape(-1, 2)
    timeStamp = ((np.uint64(stamp[:, 0]) << 17) + (stamp[:, 1] >> 15)) / 8. # time in nanoseconds.
    detector = stamp[:, 1] & 0xf
    return timeStamp, detector

print("parsing "+ filenameAlice)
timeStampAlice, detectorAlice = parseStamp(filenameAlice)
np.save('../data/timeStampAlice', timeStampAlice)
np.save('../data/detectorAlice', detectorAlice)

print("parsing "+ filenameBob)
timeStampBob, detectorBob = parseStamp(filenameBob)
np.save('../data/timeStampBob', timeStampBob)
np.save('../data/detectorBob', detectorBob)