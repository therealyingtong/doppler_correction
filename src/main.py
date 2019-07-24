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

key = Key(
    filenameAlice,
    filenameBob,
    filenameTLE,
    filenameSavedPass,
    tau,
    f
)

# parse satellite info
key.parseSatellite()

# doppler
key.calcDoppler()
key.plotDoppler()

# # parse timestamps
# key.parseStamp()

# # process timestamps
# key.processStamps()
# key.plotStamps()

# # cross-correlation
# key.xcorr()
# key.plotXcorr()

