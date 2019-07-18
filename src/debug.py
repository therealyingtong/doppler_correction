import numpy as np
from obspy.core import read
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft, fftshift
#matplotlib inline

import helper

def calcG2(timeStampAlice, timeStampBob, offsetInt, tau):
            
    offset = abs(offsetInt)

    tArray = np.arange(-offset, offset, tau)
    print('len(tArray)', len(tArray))
    g2 = np.zeros(len(tArray))

    indexStart = 0
    array1, array2 = helper.sortArrLen(timeStampAlice, timeStampBob)
    # array1, array2 = helper.sortArrLen(self.timeStampAlice, self.timeStampBob)

    for i in np.arange(0, len(array1)):    

        for j in np.arange(indexStart, len(array2)):

            diff = abs(array2[j] - array1[i])

            if diff >= offset:
                print('i', i, 'j', j, 'diff', diff, 'offset', offset, 'cont')
                indexStart = j               
                continue
            
            if diff <= offset:
                print('i', i, 'j', j, 'diff', diff, 'offset', offset, 'break')
                break
            
            #if max(self.g2) > 5*numpy.mean(self.g2):
                #   break
            
            try:
                print('index', int(diff - offset))
                print(g2[ int(diff - offset)])
                g2[ int(diff - offset)] +=1
            except IndexError:
                print('len(g2)', len(g2), 'index', int(diff - shift) )
                # pass
        #i+=1
        plt.plot(tArray, g2)
        plt.show()

timeStampAlice = [0,1,2,3,4,5,6,7,8]
timeStampBob = [0,0,0,0,1,2,3,4,5]
offset = 2
tau = 1

calcG2(timeStampAlice, timeStampBob, offset, tau)