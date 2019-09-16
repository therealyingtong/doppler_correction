#dynamic time warping
import stampProcessor
import numpy as np

mode = 'propagationDelayCorrection'
coarseTau = 10000
shift = -51318536.0
# We define two sequences x, y as numpy array
# where y is actually a sub-sequence from x
timeStampAlice = np.load('../data/aliceBobtimeStampAlice.npy')
timeStampBob = np.load('../data/aliceBobtimeStampBob.npy')
coarseTimebinAlice = stampProcessor.timebin(coarseTau, timeStampAlice)
coarseTimebinBob = stampProcessor.timebin(coarseTau, timeStampBob)

s1 = coarseTimebinAlice[500000:505000]
s2 = coarseTimebinAlice[500000:505000]
print('len(x)', len(s1))
print('len(y)', len(s2))

from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis

path = dtw.warping_path(s1, s2)
dtwvis.plot_warping(s1, s2, path, filename="warp.png")

d, paths = dtw.warping_paths(s1, s2, window=25, psi=2)
best_path = dtw.best_path(paths)
dtwvis.plot_warpingpaths(s1, s2, paths, best_path, filename="path.png")