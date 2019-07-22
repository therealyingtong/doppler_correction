#import dataGenerator
import helper
import numpy as np
import time
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt

import random
from scipy.linalg import toeplitz

import pyximport; pyximport.install()


class KeyGenerator:
    
    def __init__(self, filenameAlice = [], filenameBob=[], inputMode = "bin64", margin = 32):
        self.filenameAlice=filenameAlice
        self.filenameBob=filenameBob
        self.t0 = 0
        self.margin = margin
        self.inputMode = inputMode

    def parseStamp(self, filename):
        openedFile = open(filename, 'rb')
        stamp = np.fromfile(file=openedFile, dtype='<u4').reshape(-1, 2)
        timeStamp = ((np.uint64(stamp[:, 0]) << 17) + (stamp[:, 1] >> 15)) / 8. # time in nanoseconds.
        detector = stamp[:, 1] & 0xf
        return timeStamp, detector

    def processStamp(self, tau):

        # manually remove anomalies in timeStampBob
        self.timeStampBob = self.timeStampBob[0: int( 8.2*len(self.timeStampBob)/14 )]

        # self.interval = min([len(self.timeStampAlice), len(self.timeStampBob)])
        # self.timeStampAlice = self.timeStampAlice[0:self.interval]
        # self.timeStampBob = self.timeStampBob[0:self.interval]

        # minTime = helper.findMinOfTwoArrays(self.timeStampAlice, self.timeStampBob)
        # print('minTime', minTime)
        self.timeStampAlice = self.timeStampAlice - min(self.timeStampAlice)
        print('self.timeStampAlice[0:10]', self.timeStampAlice[0:10])

        self.timeStampBob = self.timeStampBob - min(self.timeStampBob)
        print('self.timeStampBob[0:10]', self.timeStampBob[0:10])

        self.timebinAlice = helper.timebin(self.timeStampAlice, tau)
        self.timebinBob = helper.timebin(self.timeStampBob, tau)

        # trim leading and trailing zeros
        self.timebinAlice = np.trim_zeros(self.timebinAlice)
        self.timebinBob = np.trim_zeros(self.timebinBob) 

        # normalise timebins
        # self.timebinAlice = self.timebinAlice / np.linalg.norm(self.timebinAlice)
        # self.timebinBob = self.timebinBob / np.linalg.norm(self.timebinBob)
        self.timebinAlice = self.timebinAlice - np.mean(self.timebinAlice)
        self.timebinBob = self.timebinBob - np.mean(self.timebinBob)

        # # pad arrays to same size
        self.timebinAlice, self.timebinBob = helper.padFFT(self.timebinAlice, self.timebinBob)

        self.timebinAlice = self.timebinAlice[10:]
        self.timebinBob = self.timebinBob[10:]


    def plotXcorr(self):

        print('starting plotXcorr')

        array1, array2 = helper.sortArrLen(self.timebinAlice, self.timebinBob)

        # self.timeStampAlice, self.timeStampBob = helper.padXcorr(self.timeStampAlice, self.timeStampBob)
        # array1, array2 = helper.sortArrLen(self.timeStampAlice, self.timeStampBob)

        # self.xcorr = np.correlate(array1, array2, 'full')
        # print('xcorr', self.xcorr)
        # np.save('xcorr', self.xcorr)

        # plt.plot(self.xcorr)

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

    def plotAlice(self):
        
        plt.plot(
            # self.timebinAlice, 
            self.timeStampAlice,
            marker = 'o' , 
            markersize = 2,
            # linestyle = "None"
        )
        plt.xlabel("Timestamps")
        plt.ylabel("Events")
        plt.savefig("../paper/assets/alice.png", bbox_inches = 'tight')

    def plotAlice_bin(self):
        
        plt.plot(
            self.timebinAlice, 
            # self.timeStampAlice,
            marker = 'o' , 
            markersize = 2,
            # linestyle = "None"
        )
        plt.xlabel("Timebins")
        plt.ylabel("Events")
        plt.savefig("../paper/assets/alice_bin.png", bbox_inches = 'tight')


    def plotBob(self):
        plt.plot(
            # self.timebinBob, 
            self.timeStampBob,
            marker = 'o', 
            markersize = 2,
            # linestyle = "None"
        )
        plt.xlabel("Timestamps")
        plt.ylabel("Events")
        plt.savefig("../paper/assets/bob.png", bbox_inches = 'tight')

    def plotBob_bin(self):
        plt.plot(
            self.timebinBob, 
            # self.timeStampBob,
            marker = 'o', 
            markersize = 2,
            # linestyle = "None"
        )
        plt.xlabel("Timebins")
        plt.ylabel("Events")
        plt.savefig("../paper/assets/bob_bin.png", bbox_inches = 'tight')

    def plotCC(self):
        print('starting plotCC')
        np.save('fourierXcorr', self.cc_norm)
        print('saved self.cc')
        plt.plot(
            self.zero_index - np.linspace(0,len(self.cc_norm), len(self.cc_norm)), 
            self.cc_norm, 
            '-sk', markersize = 5
        )
        print('plotted plotCC')
        plt.xlabel("Delay (ns)")
        plt.ylabel("Coincidence detections")
        plt.title("Offset = " + str(
            (self.zero_index - np.argmax(self.cc_norm))) + "ns")
        plt.annotate(str(self.shift), xy=(self.shift, 0))
        # plt.grid(True)
        plt.savefig("../paper/assets/cc.png", bbox_inches = 'tight')

    def plotCC_bin(self):
        print('starting plotCC_bin')
        # np.save('fourierXcorr_bin', self.cc_bin)
        print('saved self.cc_bin')
        plt.plot(
            self.zero_index_bin - np.linspace(0,len(self.cc_bin_norm), len(self.cc_bin_norm)), 
            self.cc_bin_norm, 
            '-sk', markersize = 5
        )
        print('plotted plotCC_bin')
        plt.xlabel("Delay (" + str(self.tau) + "ns)")
        plt.ylabel("Coincidence detections")
        # plt.title("Offset = " + str(
        #     (self.zero_index_bin - np.argmax(self.cc_bin_norm)) * self.tau) + "ns")
        # plt.annotate(str(self.shift_bin), xy=(self.shift_bin, 0))
        # plt.grid(True)
        plt.savefig("../paper/assets/cc_bin.png", bbox_inches = 'tight')



if __name__ == "__main__":
    k = KeyGenerator("../tableTopDemoData/atomicClock/ALICE_12Apr_19_3", "../tableTopDemoData/atomicClock/BOB_12Apr_19_3", '-X')
    timeStampAlice, detectorAlice = k.parseStamp(k.filenameAlice)
    k.timeStampAlice = np.copy(timeStampAlice)
    # k.timeStampBob = np.copy(timeStampAlice)
    # k.timeStampBob = k.timeStampBob[700000:len(timeStampAlice)]
    k.timeStampBob, k.detectorBob = k.parseStamp(k.filenameBob)
    k.tau = 100000

    k.processStamp(tau = k.tau)

    print('min(k.timeStampAlice)', min(k.timeStampAlice))
    print('max(k.timeStampAlice)', max(k.timeStampAlice))
    print('len(k.timeStampAlice)', len(k.timeStampAlice))

    print('min(k.timeStampBob)', min(k.timeStampBob))
    print('max(k.timeStampBob)', max(k.timeStampBob))
    print('int(len(k.timeStampBob))', int(len(k.timeStampBob)))

    f = plt.figure(1)
    k.plotAlice_bin()
    f.show()

    g = plt.figure(2)
    k.plotBob_bin()
    g.show()

    k.zero_index_bin, k.shift_bin, k.cc_bin = helper.compute_shift(k.timebinAlice, k.timebinBob)

    k.cc_bin_norm = k.cc_bin / np.linalg.norm(k.cc_bin)

    k.offset_bin = k.shift_bin * k.tau 
    print('offset_bin', k.offset_bin, 'ns')
    print('k.cc_bin[0:10]', k.cc_bin[0:10])


    # k.timeStampAlice, k.timeStampBob = helper.padFFT(k.timeStampAlice, k.timeStampBob)

    # f = plt.figure(3)
    # k.plotAlice()
    # f.show()

    # g = plt.figure(4)
    # k.plotBob()
    # g.show()
    
    # k.zero_index, k.shift, k.cc = helper.compute_shift(k.timeStampAlice, k.timeStampBob)
    # k.cc_norm = k.cc / np.linalg.norm(k.cc)

    # # k.offset = k.shift
    # # print('offset', k.offset, 'ns')
    # # print('k.cc[0:10]', k.cc[0:10])

    # # h = plt.figure(5)
    # # k.plotCC()
    # # h.show()

    p = plt.figure(6)
    k.plotCC_bin()
    p.show()

    plt.show()
