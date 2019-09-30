import sys
import correction
import stampProcessor
import xcorrProcessor
import numpy as np
import matplotlib.pyplot as plt

# load data
filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
filenameTLE = sys.argv[3]
filenameSavedPass = sys.argv[4]
mode = sys.argv[5] # unshiftedGuess, propagationDelayGuess, clockDriftShiftGuess, or aliceBobGuess

deg = 2
rateA = 5e-50 * 10
rateB = 5e-42 * 10
rateC = 5e-20 * 10
rates = [ rateB, rateC]
epsilon = 0.000001
units = 1e-9
coarseTau = 10000
sat, loc, startTime = stampProcessor.parseSatellite(filenameTLE, filenameSavedPass)

timeStampAlice = np.load(filenameAlice)
timeStampBob = np.load(filenameBob)

print("=========== doppler shift ansatz ============")
timeStampBobAnsatz, coeffsAnsatz = correction.ansatz(
	sat, loc, startTime, timeStampBob, units, deg
)

coeffs = correction.paramSearch(
	rates, epsilon,
	coeffsAnsatz,
	timeStampAlice, timeStampBob, coarseTau, mode
)

print(coeffs)