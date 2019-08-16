import sys
import numpy as np
import stampParser 
import stampProcessor 
import satParser 
import dopplerProcessor
import xcorrProcessor 
import dopplerShift 

# load data
filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
filenameTLE = sys.argv[3]
filenameSavedPass = sys.argv[4]
mode = sys.argv[5] # unshifted, propagationDelay, clockDriftShift, or aliceBob

coarseTau = 100000
coarseTauRatio = 1000
tau = coarseTau / coarseTauRatio
units = 1e-9
clockOffset = 1000000
clockDrift = 2e-6 #(2us / s)

sat, loc, startTime = satParser.parseSatellite(filenameTLE, filenameSavedPass)
timeStampAlice, detectorAlice = stampParser.parseStamp(filenameAlice)
timeStampBob, detectorBob = stampParser.parseStamp(filenameBob)
timeStampBob = stampProcessor.removeAnomalies(timeStampBob)

timeStampAlice, timeStampBob = stampProcessor.setStart(
	timeStampAlice, timeStampBob
)


# doppler
if (mode == 'propagationDelay' or 'clockDriftShift'):

	nt_list, delay_list, df_list = dopplerProcessor.calcDoppler(
		sat, loc, startTime, timeStampAlice, units
	)
	dopplerProcessor.plotDoppler(nt_list, delay_list, df_list)

	aliceShifted = dopplerShift.propagationDelay(
		timeStampAlice, nt_list, delay_list, clockOffset
	)

	if (mode == 'clockDriftShift'):
		aliceShifted = dopplerShift.clockDriftShift(
			aliceShifted, nt_list, df_list, clockDrift
		)

print("=====================COARSE=====================")

# cross-correlation
if (mode == 'unshifted'):
	coarseTimebinAlice, coarseTimebinBob = stampProcessor.timebin(coarseTau, timeStampAlice, timeStampAlice)
elif (mode == 'propagationDelay' or 'clockDriftShift'):
	coarseTimebinAlice, coarseTimebinBob = stampProcessor.timebin(coarseTau, timeStampAlice, aliceShifted)
elif (mode == 'aliceBob'):
	coarseTimebinAlice, coarseTimebinBob = stampProcessor.timebin(coarseTau, timeStampAlice, timeStampBob)

zeroIdxCoarse, shiftCoarse, maxIdxCoarse, ccCoarse = xcorrProcessor.xcorr(
	coarseTimebinAlice, coarseTimebinBob, coarseTau
)

# plot
stampProcessor.plotStamps(timeStampAlice, timeStampBob, coarseTimebinAlice, coarseTimebinBob, mode)
xcorrProcessor.plotXcorr(ccCoarse, coarseTau, zeroIdxCoarse, mode)

print("=====================FINE=====================")

maxIdx = maxIdxCoarse * coarseTauRatio
print('maxIdx', maxIdx)

lowerSubsetRatio = (coarseTauRatio - 1)/coarseTauRatio
upperSubsetRatio = (coarseTauRatio + 1)/coarseTauRatio
subsetTimeStampAlice = timeStampAlice[int(lowerSubsetRatio*maxIdxCoarse) : int(upperSubsetRatio* maxIdxCoarse)]
subsetAliceShifted = aliceShifted[int(lowerSubsetRatio*maxIdxCoarse) : int(upperSubsetRatio* maxIdxCoarse)]
subsetTimeStampBob = timeStampBob[int(lowerSubsetRatio*maxIdxCoarse) : int(upperSubsetRatio* maxIdxCoarse)]

# cross-correlation
if (mode == 'unshifted'):
	timebinAlice, timebinBob = stampProcessor.timebin(tau, subsetTimeStampAlice, subsetTimeStampAlice)
elif (mode == 'propagationDelay' or 'clockDriftShift'):
	timebinAlice, timebinBob = stampProcessor.timebin(tau, subsetTimeStampAlice, subsetAliceShifted)
elif (mode == 'aliceBob'):
	timebinAlice, timebinBob = stampProcessor.timebin(tau, subsetTimeStampAlice, subsetTimeStampBob)

print('len(timebinAlice)', len(timebinAlice))
print('len(timebinBob)', len(timebinBob))

zeroIdx, shift, maxIdx, cc = xcorrProcessor.xcorr(
	timebinAlice, timebinBob, tau
)
xcorrProcessor.plotXcorr(cc, tau, zeroIdx, mode)
