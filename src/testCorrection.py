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

rateA = 5e-42 * 10
rateB = 5e-20 * 10
epsilon = 0.000001
units = 1e-9
coarseTau = 10000
sat, loc, startTime = stampProcessor.parseSatellite(filenameTLE, filenameSavedPass)

timeStampAlice = np.load(filenameAlice)
timeStampBob = np.load(filenameBob)

print("=========== doppler shift ansatz ============")
timeStampBobAnsatz, coeffsAnsatz = correction.ansatz(
	sat, loc, startTime, timeStampBob, units
	)

a, b, c = correction.paramSearch(
	rateA, rateB, epsilon,
	coeffsAnsatz[0], coeffsAnsatz[1], coeffsAnsatz[2],
	timeStampAlice, timeStampBob, coarseTau, mode
)

