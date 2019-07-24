import numpy as np
import time
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt

import random
from scipy.linalg import toeplitz

import pyximport; pyximport.install()

def xcorr(self):

    def compute_shift(x, y):

        def cross_correlation_using_fft(x, y):
            print('starting f1 = fft(x)')
            f1 = fft(x)
            print('starting f2 = fft(np.flipud(y))')
            f2 = fft(np.flipud(y))
            print('starting cc = np.real(ifft(f1 * f2))')
            cc = np.real(ifft(f1 * f2))
            return fftshift(cc)

        # assert len(x) == len(y)
        cc = cross_correlation_using_fft(x, y)

        # assert len(cc) == len(x)
        zero_index = int(len(x) / 2) - 1
        shift = zero_index - np.argmax(cc)
        print('zero_index', zero_index)
        print('cc[zero_index]', cc[zero_index])
        print('cc[np.argmax(cc)]', cc[np.argmax(cc)])
        print('np.argmax(cc)', np.argmax(cc))
 
        return zero_index, shift, cc

    print("starting xcorr")
    self.zero_idx, self.shift, self.cc = compute_shift(
        self.timebinAlice, self.timebinBob
    )
    np.save('../data/cc', self.cc)
    self.offset = self.shift * self.tau


def plotXcorr(self):
    print('saved self.cc')
    plt.figure(5)
    plt.plot(
        self.zero_idx - np.linspace(0, len(self.cc), len(self.cc)), 
        self.cc, 
        '-sk', markersize = 5
    )
    print('plotted plotCC')
    plt.xlabel("Delay (" + str(self.tau) + "ns)")
    plt.ylabel("Coincidence detections")
    # plt.title("Offset = " + str(
    #     (self.zero_index_bin - np.argmax(self.cc_bin_norm)) * self.tau) + "ns")
    # plt.annotate(str(self.shift_bin), xy=(self.shift_bin, 0))
    # plt.grid(True)
    plt.savefig("../paper/assets/cc.png", bbox_inches = 'tight')

