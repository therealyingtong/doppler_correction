import numpy as np
from obspy.core import read
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft, fftshift
#matplotlib inline

import helper

from scipy import signal
t1 = np.linspace(-1, 1, 2 * 100, endpoint=False)
sig1 = range(0, len(t1))
plt.figure(figsize=(10,8))
plt.plot(t1, sig1, 'r')
plt.show()

def nextpow2(i):
    '''
    Find the next power 2 number for FFT
    '''

    n = 1
    while n < i: n *= 2
    return n

def shift_signal_in_frequency_domain(datin, shift):
    '''
    This is function to shift a signal in frequency domain. 
    The idea is in the frequency domain, 
    we just multiply the signal with the phase shift. 
    '''
    Nin = len(datin) 

    # get the next power 2 number for fft
    N = nextpow2(Nin +np.max(np.abs(shift)))

    # do the fft
    fdatin = np.fft.fft(datin, N)

    # get the phase shift, shift here is D in the above explanation
    ik = np.array([2j*np.pi*k for k in range(0, N)]) / N 
    fshift = np.exp(-ik*shift)

    # multiple the signal with shift and transform it back to time domain
    datout = np.real(np.fft.ifft(fshift * fdatin))

    # only get the data have the same length as the input signal
    datout = datout[0:Nin]

    return datout



# This is the amount we will move
nShift = 50

# generate the 2nd signal
sig2 = shift_signal_in_frequency_domain(sig1, nShift)

# plot two signals together
plt.figure(figsize=(10,8))
plt.plot(sig1, 'r', label = 'signal 1')
plt.plot(sig2, 'b', label = 'signal 2')
plt.legend()
plt.show()

calculate_shift = helper.compute_shift(sig1, sig2)
print('The shift we get from cross correlation is %d, the true shift should be 50'%calculate_shift)