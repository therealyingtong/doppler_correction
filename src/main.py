import sys
import numpy as np
import stampParser 
import stampProcessor 
import satParser 
import dopplerProcessor
import xcorrProcessor 
from dopplerShift import DopplerShift

# load data
filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
filenameTLE = sys.argv[3]
filenameSavedPass = sys.argv[4]
mode = sys.argv[5] # unshifted, propagationDelay, clockDriftShift, or aliceBob

tau = 1000
coarseTau = 100000
units = 1e-9
clockOffset = 1000000
clockDrift = 3e-3 #(2ms / s)

sat, loc, startTime = satParser.parseSatellite(filenameTLE, filenameSavedPass)
timeStampAlice, detectorAlice = stampParser.parseStamp(filenameAlice)
timeStampBob, detectorBob = stampParser.parseStamp(filenameBob)

if (mode != 'unshifted'):
	timeStampBob = stampProcessor.removeAnomalies(timeStampBob)

timeStampAlice, timeStampBob = stampProcessor.setStart(
	timeStampAlice, timeStampBob
)

if (mode == 'propagationDelay' or 'clockDriftShift'):
	# doppler
	nt_list, delay_list, df_list = dopplerProcessor.calcDoppler(
		sat, loc, startTime, timeStampAlice, units
	)
	dopplerProcessor.plotDoppler(nt_list, delay_list, df_list)

	dopplerShift = DopplerShift(
		timeStampAlice,
		clockOffset,
		clockDrift,
		tau,
		units,
		nt_list,
		delay_list,
		df_list
	)
	dopplerShift.propagationDelay()
	if (mode != 'propagationDelay'):
		dopplerShift.clockDriftShift()

	aliceShifted = dopplerShift.shiftedTimeStamp

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