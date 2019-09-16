import correction
import stampProcessor
import xcorrProcessor
import numpy as np
import matplotlib.pyplot as plt

mode = 'aliceBobCorrection'
coarseTau = 10000
shift = -51319056.0
timeStampAlice = np.load('../data/aliceBobtimeStampAlice.npy')
timeStampBob = np.load('../data/aliceBobtimeStampBob.npy')

correctedTimeStampBob = correction.linearShift(timeStampBob, shift)

# timeStampAlice = np.load('../data/propagationDelayTimeStampAlice.npy')
# timeStampBob = np.load('../data/propagationDelayTimeStampBob.npy')

# a = 1.16261386e-16
# b = -2.22268657e-06
# c = 2.24977492e+06

correctedTimeStampBob = correction.quadShift(timeStampBob, 0, 0, shift)


print("=====================FFT=====================")
# the coarse xcorr gives an estimate of the delay to

## coarse cross-correlation
# coarseTimebinAlice, coarseTimebinBob = stampProcessor.timebin(coarseTau, timeStampAlice, timeStampBob)
coarseTimebinAlice = stampProcessor.timebin(coarseTau, timeStampAlice)
coarseTimebinBob = stampProcessor.timebin(coarseTau, correctedTimeStampBob)


ccCoarse, coarseShift = xcorrProcessor.xcorrFFT(
	coarseTimebinAlice, coarseTimebinBob, coarseTau
)

xcorrProcessor.plotXcorr(ccCoarse, coarseTau, 0, mode)

print("=====================FINE=====================")
coarseDelay = int( coarseShift * coarseTau )
print('coarseDelay', coarseDelay)

window = 1000
startIdx = coarseDelay - window
endIdx = coarseDelay + window
binNum = window / 4 #8.0ns
fineTau = (endIdx - startIdx)/binNum #fine bin size
bins = np.linspace(startIdx, endIdx, binNum)

print('startIdx, endIdx', startIdx, endIdx)
print('bin size (ns)', fineTau )

ccFine, fineShift = xcorrProcessor.xcorr(timeStampAlice, correctedTimeStampBob, bins)
 
print('np.argmax(cc) ', np.argmax(ccFine) )
fineDelay = fineShift * fineTau + coarseDelay
print('fineDelay', fineDelay)
xcorrProcessor.plotXcorr(ccFine, fineTau, coarseDelay / fineTau, mode)