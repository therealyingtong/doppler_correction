import sys
import numpy as np

from key import Key

# load data
filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
filenameTLE = sys.argv[3]
filenameSavedPass = sys.argv[4]
tau = 100000
f = 1e9
units = 1e-9

key = Key(
    filenameAlice,
    filenameBob,
    filenameTLE,
    filenameSavedPass,
    tau,
    f,
	units
)

# parse satellite info
key.parseSatellite()

# parse timestamps
key.parseStamp()

# process timestamps
key.processStamps()

# # doppler
key.calcDoppler()
key.shiftDoppler()
key.plotDoppler()

# cross-correlation
key.binStamps()
key.xcorr()

# plot
key.plotStamps()
key.plotXcorr()
