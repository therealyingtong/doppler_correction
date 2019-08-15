import numpy as np
import time
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt

import random
from scipy.linalg import toeplitz

import pyximport; pyximport.install()

def xcorr(x, y, tau):

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

		# assert len(cc) == len(x)
		zero_index = int(len(x) / 2) - 1
		shift = zero_index - np.argmax(cc)
		return zero_index, shift, cc

	print("starting xcorr")
	zero_idx, shift, cc = compute_shift(
		x, y
	)
	np.save('../data/cc', cc)
	offset = shift * tau
	print('offset', offset, 'ns')

	max_idx = np.argmax(cc)
	print('max_idx', max_idx)
	return zero_idx, shift, max_idx, cc

def plotXcorr(cc, tau, zero_idx, title):
	plt.figure()
	max_idx = np.argmax(cc)
	start_idx = int(max_idx - len(cc) / (tau /10))
	end_idx = int(max_idx + len(cc) / (tau / 10))
	length = end_idx - start_idx 
	plt.plot(
		zero_idx - np.linspace(start_idx, end_idx, length), 
		cc[start_idx:start_idx + length], 
		'-sk', markersize = 5
	)
	print('plotted cc')
	plt.xlabel("Delay (" + str(tau) + "ns)")
	plt.ylabel("Coincidence detections")
	plt.savefig("../paper/assets/"+title+"_cc.png", bbox_inches = 'tight')
	plt.close()

