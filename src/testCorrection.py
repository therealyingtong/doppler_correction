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

units = 1e-9
coarseTau = 10000
sat, loc, startTime = stampProcessor.parseSatellite(filenameTLE, filenameSavedPass)

timeStampAlice = np.load(filenameAlice)
timeStampBob = np.load(filenameBob)

print("=========== doppler shift ansatz ============")
timeStampBob, coeffsAnsatz = correction.ansatz(
	sat, loc, startTime, timeStampBob, units
	)

print("=====================FFT=====================")
# the coarse xcorr gives an estimate of the delay to

# coarse cross-correlation
coarseTimebinAlice = stampProcessor.timebin(coarseTau, timeStampAlice)
coarseTimebinBob = stampProcessor.timebin(coarseTau, timeStampBob)

ccCoarse, coarseShift = xcorrProcessor.xcorrFFT(
	coarseTimebinAlice, coarseTimebinBob, coarseTau
)

# plot
# stampProcessor.plotStamps(timeStampAlice, timeStampBob, coarseTimebinAlice, coarseTimebinBob, mode)
xcorrProcessor.plotXcorr(ccCoarse, coarseTau, 0, mode)

print("=====================FINE=====================")
coarseDelay = int( coarseShift * coarseTau )
print('coarseDelay', coarseDelay)

window = 10000
startIdx = coarseDelay - window
endIdx = coarseDelay + window
binNum = window / 4 # 8.0ns
fineTau = (endIdx - startIdx)/binNum #fine bin size
bins = np.linspace(startIdx, endIdx, binNum)

print('startIdx, endIdx', startIdx, endIdx)
print('bin size (ns)', fineTau )

ccFine, fineShift = xcorrProcessor.xcorrFine(timeStampAlice, timeStampBob, bins)
 
print('np.argmax(cc) ', np.argmax(ccFine) )
fineDelay = fineShift * fineTau + coarseDelay
print('fineDelay', fineDelay)
xcorrProcessor.plotXcorr(ccFine, fineTau, coarseDelay / fineTau, mode)

