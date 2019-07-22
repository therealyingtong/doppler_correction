# parse binary data

import numpy as np

def parseStamp(filename):
    print("parsing "+ filename)
    openedFile = open(filename, 'rb')
    stamp = np.fromfile(file=openedFile, dtype='<u4').reshape(-1, 2)
    timeStamp = ((np.uint64(stamp[:, 0]) << 17) + (stamp[:, 1] >> 15)) / 8. # time in nanoseconds.
    detector = stamp[:, 1] & 0xf
    return timeStamp, detector

