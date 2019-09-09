import numpy as np

def linearShift(timeStamp, shift):
	shifted = timeStamp - shift
	return np.array(shifted)

def quadShift(timeStamp, a, b, c):
	shifted = timeStamp.copy()
	for i in range(len(shifted)):
		t = timeStamp[i]
		shifted[i] = t - (a*t*t + b*t+ c)
	return shifted

def paramSearch(_a, _b, _c):
	# maximise: 2*corr[M] - corr[M-1] - corr[M+1]
	# where M = np.argmax(corr)

	return a, b, c