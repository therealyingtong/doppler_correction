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
	np.save('../data/cc', cc)

	zero_idx = np.floor(len(cc)/2)
	shift = zero_idx - np.argmax(cc)
	print('shift', shift)

	return cc, shift

def plotXcorr(cc, tau, zero_value, title):

	zero_idx = np.floor(len(cc)/2)
	start_idx = np.argmax(cc) - 50 
	end_idx = np.argmax(cc) + 50

	plt.plot(
		zero_idx - np.array(range(len(cc)))[start_idx:end_idx] + zero_value,
		cc[start_idx:end_idx],
		'-sk', markersize = 5
	)
	plt.xlabel("Delay (" + str(tau) + "ns)")
	plt.ylabel("Coincidence detections")
	plt.savefig("../paper/assets/"+title+"_cc.png", bbox_inches = 'tight')
	print('plotted cc')

	plt.close()


# def plotXcorr(cc, tau, title):

# 	zero_idx = np.floor(len(cc) / 2) 

# 	max_idx = np.argmax(cc) 

# 	shift = zero_idx - max_idx 
# 	print('shift', shift)

# 	start_idx = 0
# 	end_idx = len(cc)
# 	# start_idx = int(max_idx -50)
# 	# end_idx = int(max_idx + 50)

# 	print('xcorr start_idx', start_idx)
# 	print('xcorr end_idx', end_idx)

# 	length = end_idx - start_idx 

# 	plt.plot(cc)
# 	# plt.plot(
# 	# 	np.linspace(start_idx, end_idx - 1, length) - zero_idx, 
# 	# 	cc[start_idx:start_idx + length], 
# 	# 	'-sk', markersize = 5
# 	# )
# 	plt.xlabel("Delay (" + str(tau) + "ns)")
# 	plt.ylabel("Coincidence detections")
# 	plt.savefig("../paper/assets/"+title+"_cc.png", bbox_inches = 'tight')
# 	print('plotted cc')

# 	plt.close()