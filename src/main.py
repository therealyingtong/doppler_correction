import sys
import numpy as np
from dopplerShift import DopplerShift

from key import Key

# load data
filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
filenameTLE = sys.argv[3]
filenameSavedPass = sys.argv[4]
tau = 100000
# tau = 1000000
f = 1e9
units = 1e-9
clockOffset = 1000000
clockDrift = 0.1

key = Key(
    filenameAlice,
    filenameBob,
    filenameTLE,
    filenameSavedPass,
    tau,
    f,
	units,
	clockOffset,
	clockDrift
)

# parse satellite info
key.parseSatellite()

# parse timestamps
key.parseStamp()

# process timestamps
key.processStamps()

# # doppler
key.calcDoppler()
key.plotDoppler()

dopplerShift = DopplerShift(
	key.timeStampAlice,
	clockOffset,
	clockDrift,
	key.tau,
	key.units,
	key.nt_list,
	key.delay_list,
	key.df_list
)
dopplerShift.firstOrderDopplerShift()
dopplerShift.secondOrderDopplerShift()
aliceShifted = dopplerShift.shiftedTimeStamp

# cross-correlation
key.binStamps(key.timeStampAlice, aliceShifted)

# dopplerShift.shiftedTimebin = key.timebinBob
# dopplerShift.secondOrderDopplerShift()
# key.timebinBob = dopplerShift.shiftedTimebin

key.xcorr()

# plot
key.plotStamps()
key.plotXcorr()
