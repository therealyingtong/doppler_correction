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
        # self.timeStampBob = self.timeStampBob[0: int( 8.2*len(self.timeStampBob)/14 )]

        # self.interval = min([len(self.timeStampAlice), len(self.timeStampBob)])
        # self.timeStampAlice = self.timeStampAlice[0:self.interval]
        # self.timeStampBob = self.timeStampBob[0:self.interval]

        minTime = helper.findMinOfTwoArrays(self.timeStampAlice, self.timeStampBob)
        print('minTime', minTime)
        self.timeStampAlice = self.timeStampAlice - minTime
        print('self.timeStampAlice[0:10]', self.timeStampAlice[0:10])

        self.timeStampBob = self.timeStampBob - minTime
        print('self.timeStampBob[0:10]', self.timeStampBob[0:10])

        # self.timeStampAlice, self.timeStampBob = helper.pad(self.timeStampAlice, self.timeStampBob)

        self.timebinAlice = helper.timebin(self.timeStampAlice, tau)
        self.timebinBob = helper.timebin(self.timeStampBob, tau)

        # trim leading and trailing zeros
        self.timebinAlice = np.trim_zeros(self.timebinAlice)
        self.timebinBob = np.trim_zeros(self.timebinBob) 

        # pad arrays to same size
        self.timebinAlice, self.timebinBob = helper.pad(self.timebinAlice, self.timebinBob)

        self.timebinAlice = self.timebinAlice[10:]
        self.timebinBob = self.timebinBob[10:]


    def calcG2(self, tau = 1, stable = 0):
        
        self.tau = tau
        timer = time.time()
        
        # if stable != 0: # maximal allowed drift within some time interval 
        minDiff= (-abs(self.offsetInt) - stable)/tau
        maxDiff = (abs(self.offsetInt) + stable)/tau
        
        print('minDiff', minDiff, 'maxDiff', maxDiff)

        self.tArray = np.linspace(minDiff, maxDiff, tau)
        print('len(self.tArray)', len(self.tArray))
        self.g2 = np.zeros(tau)

        indexStart = 0
        array1, array2 = helper.sortArrLen(self.timebinAlice, self.timebinBob)
        # array1, array2 = helper.sortArrLen(self.timeStampAlice, self.timeStampBob)

        for i in np.arange(0, len(array1)):    

            for j in np.arange(indexStart, len(array2)):

                if abs(array2[j] - array1[i])  <= abs(minDiff):
                    # print('i', i, 'j', j, 'diff', array2[j] - array1[i], 'minDiff', minDiff)
                    indexStart = j               
                    continue
                
                if abs(array2[j] - array1[i])  >= abs(maxDiff):
                    # print('i', i, 'j', j, 'diff', array2[j] - array1[i], 'maxDiff', maxDiff)
                    break
                
                #if max(self.g2) > 5*numpy.mean(self.g2):
                 #   break
                
                try:
                    self.g2[ int((array2[j] - array1[i]) - minDiff)] +=1
                    # print(self.g2[ int((array2[j] - array1[i]) - minDiff)])
                except IndexError:
                    pass
            #i+=1

        print("g2 calculated in " + str(time.time()-timer) + "s!")

    def plotAlice(self):
        
        plt.plot(
            self.timebinAlice, 
            # self.timeStampAlice,
            marker = 'o' , 
            markersize = 2
        )
        plt.xlabel("Timebins")
        plt.ylabel("Events")
        plt.savefig("../paper/assets/alice.png", bbox_inches = 'tight')


    def plotBob(self):
        plt.plot(
            self.timebinBob, 
            # self.timeStampBob,
            # linestyle = 'None',
            marker = 'o', 
            markersize = 2
        )
        plt.xlabel("Timebins")
        plt.ylabel("Events")
        plt.savefig("../paper/assets/bob.png", bbox_inches = 'tight')

    def plotG2(self):
        
        plt.plot((self.tArray-min(self.tArray)),self.g2, '-sk', markersize = 5)
        plt.xlabel("Delay (ns)")
        plt.ylabel("Coincidence detections")
        plt.title("Offset = " + str(min(self.tArray)) + "ns")
        plt.grid(True)
        plt.savefig("../paper/assets/g2.png", bbox_inches = 'tight')

if __name__ == "__main__":
    k = KeyGenerator("../tableTopDemoData/atomicClock/ALICE_12Apr_19_3", "../tableTopDemoData/atomicClock/BOB_12Apr_19_3", '-X')
    timeStampAlice, detectorAlice = k.parseStamp(k.filenameAlice)
    k.timeStampAlice = np.copy(timeStampAlice)
    k.timeStampBob = np.copy(timeStampAlice)
    k.timeStampBob = k.timeStampBob[700000:len(timeStampAlice)]
    # k.timeStampBob, k.detectorBob = k.parseStamp(k.filenameBob)
    tau = 10000000

    k.processStamp(tau = tau)

    print('max(k.timeStampAlice)', max(k.timeStampAlice))
    print('len(k.timeStampAlice)', len(k.timeStampAlice))

    print('int(len(k.timeStampAlice))', int(len(k.timeStampAlice)))

    print('min(k.timeStampBob)', min(k.timeStampBob))
    print('max(k.timeStampBob)', max(k.timeStampBob))
    print('int(len(k.timeStampBob))', int(len(k.timeStampBob)))

    k.shift = helper.compute_shift(k.timebinAlice, k.timebinBob)
    print('shift',k.shift*tau, 'ns')

    k.offset = k.shift * tau 
    k.offsetInt = int(k.offset)

    f = plt.figure(1)
    k.plotAlice()
    f.show()

    g = plt.figure(2)
    k.plotBob()
    g.show()

    k.calcG2(tau = tau)

    h = plt.figure(3)
    k.plotG2()
    h.show()

    plt.show()
