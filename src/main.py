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
delay = 1000000

key = Key(
    filenameAlice,
    filenameBob,
    filenameTLE,
    filenameSavedPass,
    tau,
    f,
	units,
	delay
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
	delay,
	key.nt_list,
	key.delay_list,
	key.df_list
)
dopplerShift.shift()
aliceShifted = dopplerShift.shiftedTimeStamp

# cross-correlation
key.binStamps(key.timeStampAlice, aliceShifted)
key.xcorr()

# plot
key.plotStamps()
key.plotXcorr()
