import helper
import numpy as np
import time
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt

import random
from scipy.linalg import toeplitz

import pyximport; pyximport.install()

class XCorr:

    def __init__(self, signal1, signal2, tau):
        self.signal1 = signal1
        self.signal2 = signal2
        self.tau = tau

    def xcorr(self):
        print("starting xcorr")
        self.zero_idx, self.shift, self.cc = helper.compute_shift(
            self.signal1, self.signal2
        )
        self.offset = self.shift * self.tau

    def plotXcorr(self):

        print('starting plotXcorr')

        array1, array2 = helper.sortArrLen(self.signal1, self.signal2)

        plt.figure(4)
        plt.xcorr(
            array1, 
            array2, 
            usevlines=False, 
            normed=False, 
            )
        plt.grid(True)

        plt.xlabel("Delay (" + str(self.tau) + "ns)")
        plt.ylabel("Coincidence detections")
        # plt.title("Offset = " + (np.argmax(self.xcorr) - len(array1))*self.tau + "ns")
        plt.grid(True)
        plt.savefig("../paper/assets/xcorr.png", bbox_inches = 'tight')


    def plotCC(self):
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

