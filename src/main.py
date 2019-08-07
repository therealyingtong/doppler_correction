import sys
import numpy as np
from dopplerShift import DopplerShift

from key import Key

# load data
filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
filenameTLE = sys.argv[3]
filenameSavedPass = sys.argv[4]
mode = sys.argv[5] # unshifted, firstDoppler, secondDoppler, or aliceBob

tau = 100000
# tau = 1000000
f = 1e9
units = 1e-9
clockOffset = 1000000
clockDrift = 3e-3 #(2ms / s)

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

if (mode == 'firstDoppler' or 'secondDoppler'):
	# doppler
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
	if (mode != 'firstDoppler'):
		dopplerShift.secondOrderDopplerShift()

	aliceShifted = dopplerShift.shiftedTimeStamp

# cross-correlation
if (mode == 'unshifted'):
	key.binStamps(key.timeStampAlice, key.timeStampAlice)
elif (mode == 'firstDoppler' or 'secondDoppler'):
	key.binStamps(key.timeStampAlice, aliceShifted)
elif (mode == 'aliceBob'):
	key.binStamps(key.timeStampAlice, key.timeStampBob)

key.xcorr()

# plot
key.plotStamps(mode)
key.plotXcorr(mode)