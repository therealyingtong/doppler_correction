import numpy as np
import dopplerShiftAnsatz

def ansatz(sat, loc, startTime, timeStamp, units):

	nt_list, delay_list, df_list = dopplerShiftAnsatz.calcDoppler(
		sat, loc, startTime, timeStamp, units
	)
	unshiftedTimeStamp, coeffs = dopplerShiftAnsatz.unshiftPropagationDelay(
		timeStamp, nt_list, delay_list
	)

	return unshiftedTimeStamp, coeffs

def quadShift(timeStamp, a, b, c):
	shifted = timeStamp.copy()
	for i in range(len(shifted)):
		t = timeStamp[i]
		shifted[i] = t - (a*t*t + b*t+ c)
	return shifted

def paramSearch(_a, _b, _c, timeStampAlice, timeStampBob):
	# maximise: 2*corr[M] - corr[M-1] - corr[M+1]
	# where M = np.argmax(corr)

	a=1
	b=1
	c=1
	return a, b, c

def spread(xcorr):
	maxIdx = np.argmax(xcorr)
	spread = 2*xcorr[maxIdx] - xcorr[maxIdx - 1] - xcorr[maxIdx + 1]

	return spread