import numpy as np
import dopplerShiftAnsatz
import xcorrProcessor
import stampProcessor
import matplotlib.pyplot as plt


def ansatz(sat, loc, startTime, timeStamp, units):

	nt_list, delay_list, df_list = dopplerShiftAnsatz.calcDoppler(
		sat, loc, startTime, timeStamp, units
	)
	unshiftedTimeStamp, coeffs = dopplerShiftAnsatz.unshiftPropagationDelay(
		timeStamp, nt_list, delay_list
	)

	return unshiftedTimeStamp, coeffs

def quadUnshift(timeStamp, a, b, c):
	unshifted = timeStamp.copy()
	for i in range(len(unshifted)):
		t = timeStamp[i]
		unshifted[i] = t - (a*t*t + b*t+ c)
	return unshifted

def paramSearch(
	rateA, rateB, epsilon,
	a, b, c, 
	timeStampAlice, 
	timeStampBob,
	coarseTau,
	mode):

	print("============= starting param search ============")

	c = 0 # disregard constant offset

	unshiftedTimeStampBob1 = quadUnshift(
		timeStampBob, a, b, c
	)

	print("=========== coarse FFT =============")
	# coarse cross-correlation
	coarseTimebinAlice = stampProcessor.timebin(coarseTau, timeStampAlice)
	coarseTimebinBob = stampProcessor.timebin(coarseTau, unshiftedTimeStampBob1)

	ccCoarse, coarseShift = xcorrProcessor.xcorrFFT(
		coarseTimebinAlice, coarseTimebinBob, coarseTau
	)

	coarseDelay = int( coarseShift * coarseTau )
	print('coarseDelay', coarseDelay)

	print("=========== fine FFT 1 ================")
	window = 10000
	startIdx = coarseDelay - window
	endIdx = coarseDelay + window
	binNum = window / 8 # 16.0ns
	fineTau = (endIdx - startIdx)/binNum #fine bin size
	bins = np.linspace(startIdx, endIdx, binNum)

	print('startIdx, endIdx', startIdx, endIdx)
	print('bin size (ns)', fineTau )

	ccFine1, fineShift = xcorrProcessor.xcorrFine(timeStampAlice, unshiftedTimeStampBob1, bins)

	gain1 = spread(ccFine1)

	print("=========== fine FFT 2 ================")

	_a = a - 0.0001*a
	_b = b - 0.0001*b

	unshiftedTimeStampBob2 = quadUnshift(
		timeStampBob, _a, _b, c
	)

	ccFine2, fineShift = xcorrProcessor.xcorrFine(timeStampAlice, unshiftedTimeStampBob2, bins)

	gain2 = spread(ccFine2)

	print('gain 1', gain1)
	print('gain 2', gain2)

	ccFine = None
	iteration = 0
	while (gain2 - gain1 > epsilon):
	
		iteration += 1
		print('================ iteration: ', iteration, '===============')

		diff = gain2 - gain1
		da = diff/(_a - a)
		db = diff/(_b - b)

		a = _a
		b = _b

		_a = a + rateA*da
		_b = b + rateB*db

		print('change in a', _a - a)
		print('change in b', _b - b)

		unshiftedTimeStampBob = quadUnshift(
			timeStampBob, _a, _b, c
		)

		gain1 = gain2
		ccFine, fineShift = xcorrProcessor.xcorrFine(timeStampAlice, unshiftedTimeStampBob, bins)

		gain2 = spread(ccFine)
		
		inner = 0
		while (gain2 < gain1):
			print('gain2 - gain1', gain2 - gain1)
			inner +=1 
			print('--------------iteration', iteration, 'inner', inner, '-------------')
			_a = a + rateA*da
			_b = b + rateB*db/(2*inner)

			unshiftedTimeStampBob = quadUnshift(
				timeStampBob, _a, _b, c
			)

			ccFine, fineShift = xcorrProcessor.xcorrFine(timeStampAlice, unshiftedTimeStampBob, bins)

			gain2 = spread(ccFine)
		

		xcorrProcessor.plotXcorr(ccFine, fineTau, coarseDelay / fineTau, mode+str(iteration))

		print('gain 1', gain1)
		print('gain 2', gain2)

	return a, b, c

def spread(xcorr):
	maxIdx = np.argmax(xcorr)
	spread = 2*xcorr[maxIdx] - xcorr[maxIdx - 1] - xcorr[maxIdx + 1]

	return spread / max(xcorr)