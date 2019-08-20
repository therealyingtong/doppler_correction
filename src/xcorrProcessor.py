import numpy as np
import time
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import as_strided
import random
from scipy.linalg import toeplitz
import pycorrelate as pyc

import pyximport; pyximport.install()

def xcorr(x, y, bins):

	def padToSameLength(x, y):
		diffLen = np.abs(len(x) - len(y))
		if (len(x) > len(y)):
			y = np.concatenate([np.zeros(int(np.floor(diffLen/2))), y, np.zeros(int(np.ceil(diffLen/2)))])
		else:
			x = np.concatenate([np.zeros(int(np.floor(diffLen/2))), x, np.zeros(int(np.ceil(diffLen/2)))])
		return x, y

	x,y = padToSameLength(x,y)

	print('starting xcorr')
	print('len(x), len(y)',len(x), len(y))
	print('len(bins)',len(bins))
	cc = pyc.pcorrelate(x, y, bins)

	return cc

def xcorrFFT(x, y, tau):

	def padFFT(arr1, arr2):

		def findNextPower2(number):
			if number < 1:
				return 1
			else:
				i = 1
				while i < number:
					i = i*2
				return i

		nextPower2 = findNextPower2(max(len(arr1), len(arr2)))
		diffLen1 = nextPower2 - len(arr1)
		diffLen2 = nextPower2 - len(arr2)

		arr1 = np.concatenate([np.zeros(int(np.floor(diffLen1/2))), arr1, np.zeros(int(np.ceil(diffLen1/2)))])
		arr2 = np.concatenate([np.zeros(int(np.floor(diffLen2/2))), arr2, np.zeros(int(np.ceil(diffLen2/2)))])

		return arr1, arr2, diffLen1, diffLen2

	def compute_shift(x, y):

		def cross_correlation_using_fft(x, y):
			print('len(x)', len(x), 'len(y)', len(y))

			print('starting f1 = fft(x)')
			f1 = fft(x)

			print('starting f2 = fft(np.flipud(y))')

			f2 = fft(np.flipud(y))

			print('starting cc = np.real(ifft(f1 * f2))')
			cc = np.real(ifft(f1 * f2))
			return fftshift(cc)

		# assert len(x) == len(y)
		cc = cross_correlation_using_fft(x, y)
		print('len(cc)', len(cc))

		return cc

	# # pad arrays to same size
	x, y, padLengthX, padLengthY = padFFT(
		x, y
	)
	print("starting xcorr")
	cc = compute_shift(
		x, y
	)
	np.save('../data/cc', cc)

	return cc, padLengthX, padLengthY

def plotXcorr(cc, tau, title):

	zero_idx = np.floor(len(cc) / 2) - 1

	plt.figure()
	max_idx = np.argmax(cc)
	shift = zero_idx - max_idx
	print('shift', shift)

	# start_idx = 0
	# end_idx = len(cc)
	start_idx = int(max_idx - 50)
	end_idx = int(max_idx + 50)

	print('xcorr start_idx', start_idx)
	print('xcorr end_idx', end_idx)

	length = end_idx - start_idx 
	plt.plot(
		zero_idx - np.linspace(start_idx, end_idx - 1, length), 
		cc[start_idx:start_idx + length], 
		'-sk', markersize = 5
	)
	plt.xlabel("Delay (" + str(tau) + "ns)")
	plt.ylabel("Coincidence detections")
	plt.savefig("../paper/assets/"+title+"_cc.png", bbox_inches = 'tight')
	print('plotted cc')

	plt.close()

