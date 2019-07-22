import sys
import numpy as np

from binParser import parseStamp
from timeStampProcessor import TimeStamps
from xcorrProcessor import XCorr

filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
tau = int(sys.argv[3])

# parse files
timeStampAlice, detectorAlice = parseStamp(filenameAlice)
np.save('../data/timeStampAlice', timeStampAlice)
np.save('../data/detectorAlice', detectorAlice)

timeStampBob, detectorBob = parseStamp(filenameBob)
np.save('../data/timeStampBob', timeStampBob)
np.save('../data/detectorBob', detectorBob)

# process timestamps
timestamps = TimeStamps(timeStampAlice, timeStampBob, tau)
timestamps.processStamp()
print("saving timebinAlice")
print("saving timebinBob")
timestamps.plotAll()

# cross-correlation
xcorr = XCorr(timestamps.timebinAlice, timestamps.timebinBob, timestamps.tau)
xcorr.xcorr()
np.save('../data/cc', xcorr.cc)
# xcorr.plotXcorr()
xcorr.plotCC()
