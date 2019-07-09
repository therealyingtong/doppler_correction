# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 16:09:57 2019

@author: alloh
"""

#import dataGenerator
import numpy
import time
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt

import random
from scipy.linalg import toeplitz

import pyximport; pyximport.install()

class KeyGenerator:
    
    def __init__(self, filenameAlice = [], filenameBob=[], inputMode = "bin64"):
        self.filenameAlice=filenameAlice
        self.filenameBob=filenameBob
        self.t0 = 0
        self.inputMode = inputMode
    
    def setStartTime(self):
        self.T0 = time.time()

    def convertStamp(self, stamp):
        if stamp == '':
            return [-1, -1]
        if self.inputMode == "bin64":
            timeStamp = (int(stamp[0:57],2)-self.t0)
            basis =  int(numpy.log2(int(stamp[-5:-1],2)))
            return [timeStamp, basis]
    
        elif self.inputMode == "hex1":
            timeStamp = bin(int(stamp,16))[2:]
            timeStamp = (64-len(timeStamp))*'0' + timeStamp
            timeStamp = timeStamp[:-19]
            timeStamp = int(timeStamp,2) - self.t0
            
            basis =  int(numpy.log2(int(stamp[-2],16)))
            return [timeStamp, basis]
                    
    def calcLinkParameters(self):
        
        self.S1 = len(self.timeStampAlice)
        self.S2 = len(self.timeStampBob)
        
        
        
    def calcBalance(self):
        self.balance = [0,0,0,0]
        for i in self.basisAlice:
            self.balance[int(i)] += 1
        #for i in self.balance:
        #    i /= sum(self.balance)
        
    def calcG2(self, minDiff = -10e-3, maxDiff = 10e-3, tau = 1, stable = 0):
        
        self.tau = tau
        timer = time.time()
        
        if stable != 0: # maximal allowed drift within some time interval 
            minDiff=2e-9*(self.offsetInt - stable)
            maxDiff = 2e-9*(self.offsetInt + stable)
            
        self.tArray = numpy.linspace(minDiff, maxDiff,(int((maxDiff-minDiff)/(tau*2e-9))))
        self.g2 = numpy.zeros(int((maxDiff-minDiff)/(tau*2e-9)))
       
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
        
            
    def calcG2Shift(self, tau = 10000):
        
        self.tau = tau
        timer = time.time()
        
        def cross_correlation_using_fft(x, y):
            f1 = fft(x)
            f2 = fft(numpy.flipud(y))
            cc = numpy.real(ifft(f1 * f2))
            return fftshift(cc)
 
        def compute_shift(x, y):
            assert len(x) == len(y)
            c = cross_correlation_using_fft(x, y)

            assert len(c) == len(x)
            zero_index = int(len(x) / 2) - 1
            shift = zero_index - numpy.argmax(c)
            
            self.g2 = c
            #plt.plot(c)
            plt.show()
            return shift
            
        def timebin(arr,t):
            
            counter =0
            binnedArray = [0]

            i = 0
            while i < (len(arr)):
                if arr[i]>=counter*t:
                    counter += 1
                    binnedArray.append(0)
                    continue
                i+=1
                binnedArray[-1]+=1
            
            return list(numpy.array(binnedArray))
        
        def pad(arr1, arr2):
            
            if len(arr1)> len(arr2):
                for i in range(len(arr1)-len(arr2)):
                    arr2.append(0)
            else:
                for i in range(len(arr2)-len(arr1)):
                    arr1.append(0)
                    
            return [arr1, arr2]
        
        bob = timebin(self.timeStampBob, self.tau)
        alice = timebin(self.timeStampAlice, self.tau)

        [alice, bob] = pad(alice, bob)
        
        shift = compute_shift(alice, bob)
        
        self.offset = shift*self.tau*2e-9
        self.offsetInt = int(self.offset/(2e-9))    
    
        print("Shift:    " + str(self.offset))
        print("Shift calculated in " + str(time.time()-timer) + "s!")    
   
    
    def findOffset(self):
        self.offset = self.tArray[numpy.argmax(self.g2)]
        self.offsetInt = int(self.offset/(self.tau*2e-9))

    def basisReconciliation(self):

        self.timeStampBob = list(numpy.array(self.timeStampBob)-self.offsetInt)
        
        mini = min([len(self.timeStampAlice), len(self.timeStampBob)])
        timeStampAlice = numpy.zeros(int(0.35*mini))
        timeStampBob = numpy.zeros(int(0.35*mini))
        basisAlice = numpy.zeros(int(0.35*mini))
        basisBob = numpy.zeros(int(0.35*mini))
     
        indexStart = 0
        counter = 0
        t = time.time()
        for i in range(len(self.timeStampAlice)):    
            for j in range(indexStart,len(self.timeStampBob)):
                
                if self.timeStampBob[j] < self.timeStampAlice[i]-2*self.tau:
                    indexStart = j
                    continue
                if int(abs(self.timeStampBob[j] - self.timeStampAlice[i])) < self.tau:
                    
                    timeStampAlice[counter] = self.timeStampAlice[i]
                    basisAlice[counter]=self.basisAlice[i]
                    timeStampBob[counter]= self.timeStampBob[j]
                    basisBob[counter]=self.basisBob[j]
                    counter +=1
                if self.timeStampBob[j] > self.timeStampAlice[i]:    
                    break
        
        #[a,b,c,d] = reconcile.reconcile(self.timeStampAlice, self.timeStampBob, self.basisAlice, self.basisBob, self.tau)
        #print(len(a))
        self.timeStampBob = list(timeStampBob)[0:numpy.argmax(timeStampAlice)+1]
        self.timeStampAlice = list(timeStampAlice)[0:numpy.argmax(timeStampAlice)+1]
        self.basisAlice = list(basisAlice)[0:numpy.argmax(timeStampAlice)+1]
        self.basisBob = list(basisBob)[0:numpy.argmax(timeStampAlice)+1]
        basisAlice = []
        basisBob = []
        #print("Coincidence rate:   " + str(len(self.basisAlice)))
        self.C = len(self.basisAlice)
        self.calcBalance()
        print("basis reconciled in  " + str(time.time()-t) + "s!")         
        
        if len(self.basisAlice) == len(self.basisBob):
            
            for i in range(len(self.basisAlice)):
                if int(self.basisAlice[i]/2) == int(self.basisBob[i]/2):
                        
                        basisAlice.append(self.basisAlice[i])
                        basisBob.append(self.basisBob[i])

        self.basisBob = basisBob  
        self.basisAlice = basisAlice                
                
        self.SK = len(self.basisAlice) # sifted key
               
    def errorEstimation(self):
        
        if len(self.basisAlice) == 0:
            return 1
        
        if len(self.basisAlice) == len(self.basisBob):
            qberCounter = 0
            for i in range(len(self.basisAlice)):
                if self.basisAlice[i] != self.basisBob[i]:
                    
                    qberCounter+=1

            return qberCounter/len(self.basisAlice)
        
    def determineQBER(self):
        self.QBER = self.errorEstimation()
            
    def bitExtraction(self):
        
        for i in range(len(self.basisAlice)):
            self.basisAlice[i] = self.basisAlice[i]%2
        for i in range(len(self.basisBob)):
            self.basisBob[i] = self.basisBob[i]%2
        
    def errorCorrection(self): # https://apps.dtic.mil/dtic/tr/fulltext/u2/a557404.pdf
        
        #print("Sifted key length:   " + str(len(self.basisAlice)))
        print("Initial QBER:   " + str(self.QBER))
        
        def cascade(block1, block2, errors = 0):
            
                errors = errors
            
                if sum(block1)%2 != sum(block2)%2:
                    
                    if len(block1) >1:
                        [block1[0:int(len(block1)/2)], block2[0:int(len(block2)/2)],s1] =cascade(block1[0:int(len(block1)/2)],block2[0:int(len(block2)/2)],errors)
                        [block1[int(len(block1)/2):], block2[int(len(block2)/2):],s2] = cascade(block1[int(len(block1)/2):], block2[int(len(block2)/2):],errors)
                        errors += s1+s2
                    else:
                        for i in range(len(block1)):
                            block1[0] = block2[0]
                            errors +=1
                
                return [block1, block2, errors] 

        self.errors = 0
        e = self.errorEstimation()
        if e ==0:
            return 0
        
        
        self.s = 0
        for i in range(4):
            
            c = list(zip(self.basisAlice, self.basisBob))
            blocksize = int(0.73/e)
            blocks = int(len(self.basisAlice)/blocksize)
            B =1*blocks
            random.shuffle(c)
            self.basisAlice, self.basisBob = zip(*c)
            self.basisAlice = list(self.basisAlice)
            self.basisBob = list(self.basisBob)
            blocks = int(len(self.basisAlice)/blocksize)
            self.errors = 0
            while blocks > 1:
                blocks = int(len(self.basisAlice)/blocksize)
                
                for j in range(blocks):
                    start = j*blocksize
                    end = (j+1)*blocksize
                    
                    if j == blocks-1:
                        end = -1
                        
                    a = self.basisAlice[start:end]
                    b = self.basisBob[start:end]
                    
                    [self.basisAlice[start:end],self.basisBob[start:end],errors] = cascade(a,b)
                    self.errors +=errors
                    
                blocksize = 2*blocksize
            
            self.s += B+self.errors*numpy.ceil(numpy.log2(0.73/e)  )
                    
        self.correctedKey = len(self.basisAlice)
        
        
    def privacyAmplification(self):
        if self.basisAlice == self.basisBob:
            
            #T = toeplitz(numpy.random.randint(2, size=(len(self.basisAlice)),),numpy.random.randint(2, size=max([0,int(len(self.basisAlice)-self.s)]),))
            T = toeplitz(numpy.random.randint(2, size=(len(self.basisAlice)),),numpy.random.randint(2, size=max([0,int(len(self.basisAlice)-self.s)]),))
            self.basisAlice = numpy.matmul(numpy.transpose(T) ,numpy.transpose(numpy.matrix(self.basisAlice)))%2
            self.basisBob = numpy.matmul(numpy.transpose(T),numpy.transpose(numpy.matrix(self.basisBob)))  %2
            
            self.final = len(self.basisAlice)
        else:
            self.final = 0
    
    def determineStart(self):
        fAlice = open(self.filenameAlice, 'r')
        fBob = open(self.filenameBob, 'r')
                       
        t1 = self.convertStamp(fAlice.readline())
        t2 = self.convertStamp(fBob.readline())

        print('type(t1[0])', type(t1[0]))

        fAlice.close()
        fBob.close()

        self.t0 = min([t1[0],t2[0]])

    def getDataForTimeInterval(self, f, stampArray, bases, intervalTime, startTime):
        
        while True:
            
            stamp = self.convertStamp(f.readline())
            
            if stamp[0] == -1:
                return -1
            stampArray.append(stamp[0])
            bases.append(stamp[1])
            
            if stampArray[-1] > intervalTime:
                
                return 1
    
    def stampPreparation(self, intervalTime = 2e9):
        
        fAlice = open(self.filenameAlice, 'r')
        fBob = open(self.filenameBob, 'r')
        
        self.timeStampAlice = []
        self.basisAlice = []
        
        self.timeStampBob = []
        self.basisBob = []
        
        counter = 0
        
        while 1:
        
            end1 = self.getDataForTimeInterval(fAlice, self.timeStampAlice, self.basisAlice, intervalTime, counter*intervalTime)
            end2 = self.getDataForTimeInterval(fBob, self.timeStampBob, self.basisBob, intervalTime, counter*intervalTime)
           
            if end1== -1 and end2 == -1:
                break
            
        fAlice.close()
        fBob.close()
        
        
    def plotG2(self):
        
        plt.plot((self.tArray-min(self.tArray))*1e6,self.g2, '-sk')
        plt.xlabel("Delay (us)")
        plt.ylabel("Coincidence detections")
        plt.title("Offset = " + str(min(self.tArray)*1e3) + " ms")
        plt.grid(True)
        plt.show()
        
    def printResults(self):
        print("##############   RESULTS   ###############")
        print("Experiment time:    " + str(2e-9*int((max(self.timeStampAlice)-min(self.timeStampAlice)))))
        #print("Evaluation time:    " + str(time.time()-self.T0))
        print("S1:   " + str(self.S1))
        print("S2:   " + str(self.S2))
        print("Coinc:   " + str(self.C))
        print("Eff 1:   " + str(self.C/self.S2))
        print("Eff 2:   " + str(self.C/self.S1))
        print("\n")
        print("QBER:   " + str(self.QBER))
        print("Sifted:   " + str(self.SK))
        print("Corrected:    " + str(self.correctedKey))
        print("Final:    " + str(self.final))
        print("Final QBER:    " + str(self.errorEstimation()))

        

if __name__ == "__main__":
    k = KeyGenerator("../tableTopDemoData/beacon/20190416_10_kHZ_beaconTestAlice", "../tableTopDemoData/beacon/20190416_10_kHZ_beaconTestBob", 'hex1')
    k.setStartTime()
    k.determineStart()
    k.stampPreparation()
    print('len(k.timeStampAlice)', len(k.timeStampAlice))
    print('k.timeStampAlice', k.timeStampAlice[0:100])
    print('k.basisAlice', k.basisAlice[0:100])

    k.calcG2Shift(10000)
    k.calcG2(stable = 10000)
    k.plotG2()
    k.findOffset()

    # k.calcLinkParameters()
    # k.findOffset()
    # k.basisReconciliation()
    # k.bitExtraction()
    # k.determineQBER()
    # k.errorCorrection()
    # k.privacyAmplification()
    
    # k.printResults()
    