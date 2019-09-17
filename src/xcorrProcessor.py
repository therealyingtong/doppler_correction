import numpy as np
import time
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import as_strided
import random
import stampProcessor
from scipy.linalg import toeplitz
import pycorrelate as pyc

import pyximport; pyximport.install()

def xcorr(timeStampAlice, timeStampBob, coarseTau, mode):
	print("=====================FFT=====================")
	# the coarse xcorr gives an estimate of the delay to

	# coarse cross-correlation
	coarseTimebinAlice = stampProcessor.timebin(coarseTau, timeStampAlice)
	coarseTimebinBob = stampProcessor.timebin(coarseTau, timeStampBob)

	ccCoarse, coarseShift = xcorrFFT(
		coarseTimebinAlice, coarseTimebinBob, coarseTau
	)

	# plot
	# stampProcessor.plotStamps(timeStampAlice, timeStampBob, coarseTimebinAlice, coarseTimebinBob, mode)
	plotXcorr(ccCoarse, coarseTau, 0, mode)

	print("=====================FINE=====================")
	coarseDelay = int( coarseShift * coarseTau )
	print('coarseDelay', coarseDelay)

	window = 10000
	startIdx = coarseDelay - window
	endIdx = coarseDelay + window
	binNum = window / 4 # 8.0ns
	fineTau = (endIdx - startIdx)/binNum #fine bin size
	bins = np.linspace(startIdx, endIdx, binNum)

	print('startIdx, endIdx', startIdx, endIdx)
	print('bin size (ns)', fineTau )

	ccFine, fineShift = xcorrFine(timeStampAlice, timeStampBob, bins)
	
	print('np.argmax(cc) ', np.argmax(ccFine) )
	fineDelay = fineShift * fineTau + coarseDelay
	print('fineDelay', fineDelay)
	plotXcorr(ccFine, fineTau, coarseDelay / fineTau, mode)

def xcorrFine(x, y, bins):

	print('starting xcorr')
	print('len(x), len(y)',len(x), len(y))
	print('len(bins)',len(bins))
	cc = pyc.pcorrelate(x, y, bins)

	zero_idx = np.floor(len(cc)/2)
	shift = np.argmax(cc) - zero_idx
	print('shift', shift)

	return cc, shift

def xcorrFFT(x, y, tau):

	def findNextPower2(number):
		if number < 1:
			return 1
		else:
			i = 1
			while i < number:
				i = i*2
			return i

	def compute_shift(x, y):

		def cross_correlation_using_fft(x, y, N):
			print('len(x)', len(x), 'len(y)', len(y))
			print('N', N)

			print('starting f1 = fft(x)')
			f1 = fft(x, N)

			print('starting f2 = fft(np.flipud(y))')
			f2 = np.conj(fft(y, N))

			print('starting cc = np.real(ifft(f1 * f2))')
			cc = np.real(ifft(f1 * f2))
			return fftshift(cc)

		# assert len(x) == len(y)
		N = findNextPower2(len(x) + len(y))
		cc = cross_correlation_using_fft(x, y, N)

		return cc

	print("starting xcorr")
	cc = compute_shift(
		x, y
	)

	zero_idx = np.floor(len(cc)/2)
	shift = zero_idx - np.argmax(cc)
	print('shift', shift)

	return cc, shift

def plotXcorr(cc, tau, zero_value, title):

	zero_idx = np.floor(len(cc)/2)
	start_idx = np.argmax(cc) - 50 
	end_idx = np.argmax(cc) + 50
	# start_idx = 0
	# end_idx = len(cc)

	plt.plot(
		zero_idx - np.array(range(len(cc)))[start_idx:end_idx] + zero_value,
		cc[start_idx:end_idx],
		'-sk', markersize = 5
	)
	plt.xlabel("Delay (" + str(tau) + "ns)")
	plt.ylabel("Cross-correlation")
	plt.savefig("../paper/assets/"+title+"_cc.png", bbox_inches = 'tight')
	print('plotted cc')

	plt.close()

