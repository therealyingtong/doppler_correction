import numpy as np
import dopplerShiftAnsatz
import xcorrProcessor
import stampProcessor
import matplotlib.pyplot as plt


def ansatz(sat, loc, startTime, timeStamp, units, deg):

	nt_list, delay_list, df_list = dopplerShiftAnsatz.calcDoppler(
		sat, loc, startTime, timeStamp, units
	)
	unshiftedTimeStamp, coeffs = dopplerShiftAnsatz.unshiftPropagationDelay(
		timeStamp, nt_list, delay_list, deg
	)

	return unshiftedTimeStamp, coeffs

def unshift(timeStamp, coeffsArray):
	unshifted = timeStamp.copy()
	coeffsArrayFlipped = np.flip(coeffsArray)

	for i in range(len(unshifted)):
		t = timeStamp[i]
		shift = 0
		for j in range(len(coeffsArrayFlipped) - 1, -1, -1):
			shift = shift + coeffsArrayFlipped[j]*(t**j)
		unshifted[i] = t - shift
	return unshifted


def paramSearch(
	ratesArray,
	epsilon,
	coeffsArray, 
	timeStampAlice, 
	timeStampBob,
	coarseTau,
	timebinSize,
	mode):

	print("============= starting param search ============")

	coeffsArray[len(coeffsArray) - 1] = 0 # disregard constant offset
	print('coeffsArray', coeffsArray)

	unshiftedTimeStampBob1 = unshift(
		timeStampBob, coeffsArray
	)
	print('unshiftedTimeStampBob1', unshiftedTimeStampBob1)

	print("=========== coarse FFT =============")
	# coarse cross-correlation
	coarseTimebinAlice = stampProcessor.timebin(coarseTau, timeStampAlice)
	coarseTimebinBob = stampProcessor.timebin(coarseTau, unshiftedTimeStampBob1)

	ccCoarse, coarseShift = xcorrProcessor.xcorrFFT(
		coarseTimebinAlice, coarseTimebinBob, coarseTau
	)

	coarseDelay = int( coarseShift * coarseTau )
	print('coarseDelay', coarseDelay)

	window = 10000
	startIdx = coarseDelay - window
	endIdx = coarseDelay + window
	binNum = window / (timebinSize / 2) 
	fineTau = (endIdx - startIdx)/binNum #fine bin size
	bins = np.linspace(startIdx, endIdx, binNum)

	print("=========== fine FFT 1 ===========")

	print('startIdx, endIdx', startIdx, endIdx)
	print('bin size (ns)', fineTau )

	ccFine1, fineShift = xcorrProcessor.xcorrFine(timeStampAlice, unshiftedTimeStampBob1, bins)

	gain1 = spread(ccFine1)

	print("=========== fine FFT 2 ===========")

	coeffsArray_ = coeffsArray.copy()

	for i in range(len(coeffsArray_)):
		coeffsArray_[i] = coeffsArray[i] + 0.0001 * coeffsArray[i]

	unshiftedTimeStampBob2 = unshift(
		timeStampBob, coeffsArray_
	)

	ccFine2, fineShift = xcorrProcessor.xcorrFine(timeStampAlice, unshiftedTimeStampBob2, bins)

	gain2 = spread(ccFine2)

	if (gain1 > gain2):
		print("=========== fine FFT 2 ===========")

		coeffsArray_ = coeffsArray.copy()

		for i in range(len(coeffsArray_)):
			coeffsArray_[i] = coeffsArray[i] - 0.0001 * coeffsArray[i]

		unshiftedTimeStampBob2 = unshift(
			timeStampBob, coeffsArray_
		)

		ccFine2, fineShift = xcorrProcessor.xcorrFine(timeStampAlice, unshiftedTimeStampBob2, bins)

		gain2 = spread(ccFine2)

	print ("========= start iterations =========")

	print('gain 1', gain1)
	print('gain 2', gain2)

	ccFine = None
	iteration = 0
	while (gain2 - gain1 > epsilon):
	
		iteration += 1
		print('================ iteration: ', iteration, '===============')

		diff = gain2 - gain1
		gradients = [0] * (len(coeffsArray) - 1)

		for i in range(len(gradients)):
			if ((coeffsArray_[i] - coeffsArray[i]) == 0):
				gradients[i] = 0
			else:
				gradients[i] = diff / (coeffsArray_[i] - coeffsArray[i])

		coeffsArray = coeffsArray_.copy()

		for i in range(len(coeffsArray_) - 1):
			coeffsArray_[i] = coeffsArray_[i] + ratesArray[i]*gradients[i]

		print('change in coeffs', coeffsArray_ - coeffsArray)

		unshiftedTimeStampBob = unshift(
			timeStampBob, coeffsArray_
		)

		gain1 = gain2
		ccFine, fineShift = xcorrProcessor.xcorrFine(timeStampAlice, unshiftedTimeStampBob, bins)

		gain2 = spread(ccFine)		

		xcorrProcessor.plotXcorr(ccFine, fineTau, coarseDelay / fineTau, mode+str(iteration))

		print('gain 1', gain1)
		print('gain 2', gain2)

	return coeffsArray

def hyperparamSearch():
	return rate

def spread(xcorr):
	maxIdx = np.argmax(xcorr)
	spread = 2*xcorr[maxIdx] - xcorr[maxIdx - 1] - xcorr[maxIdx + 1]
	# spread = max(xcorr[maxIdx] - xcorr[maxIdx - 1],xcorr[maxIdx] - xcorr[maxIdx + 1])

	return spread / max(xcorr)