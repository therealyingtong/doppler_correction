import sys
import numpy as np
import stampParser 
import stampProcessor 
import satParser 
import xcorrProcessor 
import dopplerShift 
import dopplerShiftAnsatz
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

sat, loc, startTime = satParser.parseSatellite(filenameTLE, filenameSavedPass)
timeStampAlice, detectorAlice = stampParser.parseStamp(filenameAlice)
timeStampBob, detectorBob = stampParser.parseStamp(filenameBob)
timeStampBob = stampProcessor.removeAnomalies(timeStampBob)

timeStampAlice, timeStampBob = stampProcessor.setStart(
	timeStampAlice, timeStampBob
)

if (mode == 'unshifted'):
	# timeStampAlice = timeStampBob
	timeStampBob = timeStampAlice

# doppler
if (mode == 'propagationDelay' or mode == 'clockDriftShift'):

	delay_list, df_list = dopplerShift.calcDoppler(
		sat, loc, startTime, timeStampBob, units
	)
	dopplerShift.plotDoppler(timeStampBob, delay_list, df_list)

	timeStampBob = dopplerShift.propagationDelay(
		timeStampBob, delay_list
	)

	if (mode == 'clockDriftShift'):
		timeStampBob = dopplerShift.clockDriftShift(
			timeStampBob, df_list, clockDrift
		)

np.save('../data/' + mode + 'TimeStampAlice', timeStampAlice)
np.save('../data/' + mode + 'TimeStampBob', timeStampBob)

print('len(timeStampAlice)', len(timeStampAlice))
print('len(timeStampBob)', len(timeStampBob))

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

ccFine, fineShift = xcorrProcessor.xcorr(timeStampAlice, timeStampBob, bins)
 
print('np.argmax(cc) ', np.argmax(ccFine) )
fineDelay = fineShift * fineTau + coarseDelay
print('fineDelay', fineDelay)
xcorrProcessor.plotXcorr(ccFine, fineTau, coarseDelay / fineTau, mode)

