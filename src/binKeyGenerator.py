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

    def determineStart(self):
        self.t0 = min(self.timeStampAlice.tolist() + self.timeStampBob.tolist())
        print('self.t0', self.t0)
        self.timeStampAlice = self.timeStampAlice - self.t0
        self.timeStampBob = self.timeStampBob - self.t0

    def parseStamp(self, filename):
        openedFile = open(filename, 'rb')
        stamp = np.fromfile(file=openedFile, dtype='<u4').reshape(-1, 2)
        timeStamp = ((np.uint64(stamp[:, 0]) << 17) + (stamp[:, 1] >> 15)) / 8. # time in nanoseconds.
        basis = stamp[:, 1] & 0xf
        return timeStamp, basis

    def calcG2Shift(self, tau):
        self.tau = tau
        timer = time.time()
        
        def cross_correlation_using_fft(x, y):
            f1 = fft(x)
            f2 = fft(np.flipud(y))
            cc = np.real(ifft(f1 * f2))
            return fftshift(cc)
 
        def compute_shift(x, y):
            assert len(x) == len(y)
            c = cross_correlation_using_fft(x, y)

            assert len(c) == len(x)
            zero_index = int(len(x) / 2) - 1
            shift = zero_index - np.argmax(c)
            
            self.g2 = c
            #plt.plot(c)
            plt.show()
            return shift
        
        bob = helper.timebin(self.timeStampBob, self.tau)
        alice = helper.timebin(self.timeStampAlice, self.tau)
        
        [alice, bob] = helper.pad(alice, bob)
        print('len(alice)', len(alice), max(alice), sum(alice))
        print('len(bob)', len(bob), max(bob), sum(bob))

        def zero_to_nan(values):
            """Replace every 0 with 'nan' and return a copy."""
            return [float('nan') if x==0 else x for x in values]

        # plt.plot(alice)
        # plt.plot(zero_to_nan(alice))
        plt.plot(bob)
        
        shift = compute_shift(alice, bob)
        
        self.offset = shift*self.tau*2e-9
        self.offsetInt = int(self.offset/(2e-9))    
    
        print("Shift:    " + str(self.offset))
        print("Shift calculated in " + str(time.time()-timer) + "s!")    
   
    def calcG2(self, minDiff = -10e-3, maxDiff = 10e-3, tau = 1, stable = 0):
        
        self.tau = tau
        timer = time.time()
        
        if stable != 0: # maximal allowed drift within some time interval 
            minDiff=2e-9*(self.offsetInt - stable)
            maxDiff = 2e-9*(self.offsetInt + stable)
        
        self.tArray = np.linspace(minDiff, maxDiff,(int((maxDiff-minDiff)/(tau*2e-9))))
        self.g2 = np.zeros(int((maxDiff-minDiff)/(tau*2e-9)))
       
        indexStart = 0
        for i in range(0, int(len(self.timeStampAlice))):    

            for j in range(indexStart,int(len(self.timeStampBob))):

                if self.timeStampBob[j] - self.timeStampAlice[i]  <= minDiff/(2e-9):
                    indexStart = j               
                    continue
                
                if self.timeStampBob[j] - self.timeStampAlice[i]  >= maxDiff/(2e-9):
                    break
                
                #if max(self.g2) > 5*numpy.mean(self.g2):
                 #   break
                
                try:
                    self.g2[ int((self.timeStampBob[j] - self.timeStampAlice[i]) - minDiff/(2e-9))] +=1
                except IndexError:
                    pass
            #i+=1

        print("g2 calculated in " + str(time.time()-timer) + "s!")
        
    def plotG2(self):
        
        plt.plot((self.tArray-min(self.tArray))*1e6,self.g2, '-sk')
        plt.xlabel("Delay (us)")
        plt.ylabel("Coincidence detections")
        plt.title("Offset = " + str(min(self.tArray)*1e3) + " ms")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    k = KeyGenerator("../tableTopDemoData/atomicClock/ALICE_12Apr_19_3", "../tableTopDemoData/atomicClock/BOB_12Apr_19_3", '-X')
    k.timeStampAlice, k.basisAlice = k.parseStamp(k.filenameAlice)
    k.timeStampBob, k.basisBob = k.parseStamp(k.filenameBob)
    k.determineStart()

    print('k.timeStampAlice', min(k.timeStampAlice), max(k.timeStampAlice))
    print('k.timeStampBob', min(k.timeStampBob), max(k.timeStampBob))

    timebinAlice = helper.timebin(k.timeStampAlice, 100000000)
    timebinBob = helper.timebin(k.timeStampBob, 100000000)
    f = plt.figure(1)
    plt.plot(timebinAlice)
    f.show()
    g = plt.figure(2)
    # plt.plot(timebinBob[int(len(timebinBob)/2):int(1.5*len(timebinBob)/2)])
    plt.plot(timebinBob)
    g.show()

    plt.show()
    # print('len(timebinBob)', len(timebinBob), max(timebinBob), sum(timebinBob))

    # k.calcG2Shift(100000000)
    # k.calcG2(stable = 10)
    # k.plotG2()
