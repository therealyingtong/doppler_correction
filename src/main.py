import sys
import numpy as np
import stampProcessor 
import xcorrProcessor 
import dopplerShift 
import correction
import matplotlib.pyplot as plt

# load data
filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
filenameTLE = sys.argv[3]
filenameSavedPass = sys.argv[4]
mode = sys.argv[5] # unshifted, propagationDelay, clockDriftShift, or aliceBob

coarseTau = 10000 #coarse timebin size (in ns)
units = 1e-9
clockOffset = 1000000
clockDrift = 1e-6 #(1us / s)

timeStampAlice, timeStampBob = stampProcessor.process(
	filenameTLE,
	filenameSavedPass,
	filenameAlice,
	filenameBob,
	mode,
	units,
	clockDrift
)

xcorrProcessor.xcorr(
	timeStampAlice,
	timeStampBob,
	coarseTau,
	mode
)
