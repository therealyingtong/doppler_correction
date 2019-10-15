import sys
import correction
import stampProcessor
import xcorrProcessor
import numpy as np
import matplotlib.pyplot as plt

# load data
filenameAlice = sys.argv[1]
filenameBob = sys.argv[2]
filenameTLE = sys.argv[3]
filenameSavedPass = sys.argv[4]
timebinSize = int(sys.argv[5])
mode = sys.argv[6] # unshiftedGuess, propagationDelayGuess, clockDriftShiftGuess, or aliceBobGuess

deg = 2
# rateC = 5e-10 * 10
# rateB = rateC**2
# rateA = rateC**3
# ratesArray = [rateA, rateB, rateC]

rateA = 5e-90 * 0.01
rateB = 5e-62 * 0.1
rateC = 5e-42 * 0.8
rateD = 5e-20 * 0.8
# ratesArray = [rateA, rateB, rateC, rateD]
# ratesArray = [rateB, rateC, rateD]
ratesArray = [rateC, rateD]
epsilon = 0.00000001
units = 1e-9
coarseTau = 10000
sat, loc, startTime = stampProcessor.parseSatellite(filenameTLE, filenameSavedPass)

timeStampAlice = np.load(filenameAlice)
timeStampBob = np.load(filenameBob)

print("=========== doppler shift ansatz ============")
timeStampBobAnsatz, coeffsAnsatz = correction.ansatz(
	sat, loc, startTime, timeStampBob, units, deg
)


coeffs, gain, coeffsPlot = correction.paramSearch(
	ratesArray,
	epsilon,
	coeffsAnsatz,
	timeStampAlice, timeStampBob, coarseTau, timebinSize, mode
)

print(coeffs)

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = gain
x = [item[0] for item in coeffsPlot]
y = [item[1] for item in coeffsPlot]
ax.plot(x, y, z, label='gain function')
ax.legend()

plt.show()