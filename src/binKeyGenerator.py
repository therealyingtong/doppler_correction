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
        basis = stamp[:, 1] & 0xf
        return timeStamp, basis

    def processStamp(self):
        self.timebinAlice = helper.timebin(self.timeStampAlice, 10000000)
        self.timebinBob = helper.timebin(self.timeStampBob, 10000000)
        self.timebinBob = self.timebinBob[0:int(60*len(self.timebinBob)/100)]

        # trim leading and trailing zeros
        self.timebinAlice = np.trim_zeros(self.timebinAlice)
        self.timebinBob = np.trim_zeros(self.timebinBob) 

        # pad arrays to same size
        self.timebinAlice, self.timebinBob = helper.pad(self.timebinAlice, k.timebinBob)

    def calcG2(self, minDiff = -10e-3, maxDiff = 10e-3, tau = 1, stable = 0):
        
        self.tau = tau
        timer = time.time()
        
        if stable != 0: # maximal allowed drift within some time interval 
            minDiff=2e-9*(self.shift - stable)
            maxDiff = 2e-9*(self.shift + stable)
        
        self.tArray = np.linspace(minDiff, maxDiff,(int((maxDiff-minDiff)/(tau*2e-9))))
        self.g2 = np.zeros(int((maxDiff-minDiff)/(tau*2e-9)))
       
        indexStart = 0
        for i in range(0, int(len(self.timebinAlice))):    

            for j in range(indexStart,int(len(self.timebinBob))):

                if self.timebinBob[j] - self.timebinAlice[i]  <= minDiff/(2e-9):
                    indexStart = j               
                    continue
                
                if self.timebinBob[j] - self.timebinAlice[i]  >= maxDiff/(2e-9):
                    break
                
                #if max(self.g2) > 5*numpy.mean(self.g2):
                 #   break
                
                try:
                    self.g2[ int((self.timebinBob[j] - self.timebinAlice[i]) - minDiff/(2e-9))] +=1
                except IndexError:
                    pass
            #i+=1

        print("g2 calculated in " + str(time.time()-timer) + "s!")

    def plotAlice(self):
        
        plt.plot(
            self.timebinAlice, linestyle = 'None', 
            color = 'None', marker = 'o' , 
            markeredgecolor = 'k', markersize = 6
        )
        plt.xlabel("Timebins")
        plt.ylabel("Events")
        plt.savefig("../paper/assets/alice.png", bbox_inches = 'tight')


    def plotBob(self):
        plt.plot(
            k.timebinBob, linestyle = 'None', 
            color = 'None', marker = 'o', 
            markeredgecolor = 'k', markersize = 6
        )
        plt.xlabel("Timebins")
        plt.ylabel("Events")
        plt.savefig("../paper/assets/bob.png", bbox_inches = 'tight')

    def plotG2(self):
        
        plt.plot((self.tArray-min(self.tArray))*1e6,self.g2, '-sk', markersize = 5)
        plt.xlabel("Delay (us)")
        plt.ylabel("Coincidence detections")
        plt.title("Offset = " + str(min(self.tArray)*1e3) + " ms")
        plt.grid(True)
        plt.savefig("../paper/assets/g2.png", bbox_inches = 'tight')

if __name__ == "__main__":
    k = KeyGenerator("../tableTopDemoData/atomicClock/ALICE_12Apr_19_3", "../tableTopDemoData/atomicClock/BOB_12Apr_19_3", '-X')
    k.timeStampAlice, k.basisAlice = k.parseStamp(k.filenameAlice)
    k.timeStampBob, k.basisBob = k.parseStamp(k.filenameBob)

    print('k.timeStampAlice', min(k.timeStampAlice), max(k.timeStampAlice))
    print('k.timeStampBob', min(k.timeStampBob), max(k.timeStampBob))

    k.processStamp()
    k.shift = helper.compute_shift(k.timebinAlice, k.timebinBob)

    f = plt.figure(1)
    k.plotAlice()
    f.show()

    g = plt.figure(2)
    k.plotBob()
    g.show()

    k.calcG2(stable = 0)

    h = plt.figure(3)
    k.plotG2()
    h.show()
    
    plt.show()
