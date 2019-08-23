import sys
import numpy as np
import stampParser 
import stampProcessor 
import satParser 
import dopplerProcessor
import xcorrProcessor 
import dopplerShift 
import matplotlib.pyplot as plt

# load data
filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
filenameTLE = sys.argv[3]
filenameSavedPass = sys.argv[4]
mode = sys.argv[5] # unshifted, propagationDelay, clockDriftShift, or aliceBob

coarseTau = 100000 #coarse timebin size (in ns)
coarseTauRatio = 1000
tau = coarseTau / coarseTauRatio #fine timebin size (in ns)
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
print('len(timeStampAlice), len(timeStampBob)', len(timeStampAlice), len(timeStampBob))

if (mode == 'unshifted'):
	timeStampBob = timeStampAlice
# doppler
elif (mode == 'propagationDelay' or mode == 'clockDriftShift'):

	nt_list, delay_list, df_list = dopplerProcessor.calcDoppler(
		sat, loc, startTime, timeStampAlice, units
	)
	dopplerProcessor.plotDoppler(nt_list, delay_list, df_list)

	timeStampBob = dopplerShift.propagationDelay(
		timeStampAlice, nt_list, delay_list, clockOffset
	)

	if (mode == 'clockDriftShift'):
		timeStampBob = dopplerShift.clockDriftShift(
			timeStampBob, nt_list, df_list, clockDrift
		)

print("=====================FFT=====================")
# the coarse xcorr gives an estimate of the delay to

# coarse cross-correlation
coarseTimebinAlice, coarseTimebinBob = stampProcessor.timebin(coarseTau, timeStampAlice, timeStampBob)

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
binNum = 0.2*window 
fineTau = (endIdx - startIdx)/binNum
bins = np.linspace(startIdx, endIdx, binNum)

print('startIdx, endIdx', startIdx, endIdx)
print('bin size (ns)', fineTau )

ccFine, fineShift = xcorrProcessor.xcorr(timeStampAlice, timeStampBob, bins)
 
print('np.argmax(cc) ', np.argmax(ccFine) )
fineDelay = fineShift * fineTau + coarseDelay
print('fineDelay', fineDelay)
xcorrProcessor.plotXcorr(ccFine, fineTau, coarseDelay/fineTau, mode)
