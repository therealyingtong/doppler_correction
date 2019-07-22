import numpy as np
from scipy import signal
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import matplotlib.pyplot as plt
import math
import random
from scipy.linalg import toeplitz
from astropy.convolution import convolve

import pyximport; pyximport.install()

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
    
    return list(np.array(binnedArray))

def firstZeroIndex(arr):
    for i in range(len(arr)):
        print(arr[i])
        if arr[i] == 0:
            return i

def sortArrLen(arr1, arr2):
    # return arrays ordered in ascending order of array length
    if len(arr1) > len(arr2):
        return arr2, arr1
    else:
        return arr1, arr2

def findMinOfTwoArrays(arr1, arr2):
    return min([min(arr1), min(arr2)])

def padFFT(arr1, arr2):

    nextPower2 = findNextPower2(max(len(arr1), len(arr1)))
    diffLen1 = nextPower2 - len(arr1)
    diffLen2 = nextPower2 - len(arr2)

    arr1 = np.concatenate([np.zeros(math.floor(diffLen1/2)), arr1, np.zeros(math.ceil(diffLen1/2))])
    arr2 = np.concatenate([np.zeros(math.floor(diffLen2/2)), arr2, np.zeros(math.ceil(diffLen2/2))])

    return arr1, arr2

def padXcorr(arr1, arr2):

    pad = np.zeros(abs(len(arr1) - len(arr2)))

    if len(arr1)> len(arr2):
        arr1 = np.concatenate([np.zeros(len(arr2) - 1), arr1, np.zeros(len(arr2) - 1)])
        arr2 = np.concatenate([np.zeros(len(arr2) - 1), arr2, pad, np.zeros(len(arr2) - 1)])

    else:
        arr2 = np.concatenate([np.zeros(len(arr1) - 1), arr2, np.zeros(len(arr1) - 1)])
        arr1 = np.concatenate([np.zeros(len(arr1) - 1), arr1, pad, np.zeros(len(arr1) - 1)])

    return arr1, arr2

def findNextPower2(number):
    if number < 1:
        return 1
    else:
        i = 1
        while i < number:
            i = i*2
        return i

def cross_correlation_using_fft(x, y):
    print('starting f1 = fft(x)')
    f1 = fft(x)
    print('starting f2 = fft(np.flipud(y))')
    f2 = fft(np.flipud(y))
    print('starting cc = np.real(ifft(f1 * f2))')
    cc = np.real(ifft(f1 * f2))
    return fftshift(cc)

def compute_shift(x, y):
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


def calculate_time_offset_from_signals(times_A, signal_A,
                                    times_B, signal_B,
                                    plot=True, block=True):
    """ Calculates the time offset between signal A and signal B. """
    # convoluted_signals = signal.correlate(signal_B, signal_A, mode = "same")

    convoluted_signals = convolve(signal_B, signal_A[0: len(signal_A) - 1])

    dt_A = np.mean(np.diff(times_A))
    print('dt_A', dt_A)
    offset_indices = np.arange(-len(signal_A) + 1, len(signal_B))
    max_index = np.argmax(convoluted_signals)
    print('max_index', max_index)
    offset_index = offset_indices[max_index]
    print('offset_index', offset_index)
    time_offset = dt_A * offset_index + times_B[0] - times_A[0]
    print('times_B[0], times_A[0]', times_B[0], times_A[0])
    # if plot:
    #     plot_results(times_A, times_B, signal_A, signal_B, convoluted_signals,
    #                 time_offset, block=block)
    return offset_indices, time_offset, convoluted_signals


# def plot_results(times_A, times_B, signal_A, signal_B,
#                  convoluted_signals, time_offset, block=True):

#     fig = plt.figure()

#     title_position = 1.05

#     matplotlib.rcParams.update({'font.size': 20})

#     # fig.suptitle("Time Alignment", fontsize='24')
#     a1 = plt.subplot(1, 3, 1)

#     a1.get_xaxis().get_major_formatter().set_useOffset(False)

#     plt.ylabel('angular velocity norm [rad]')
#     plt.xlabel('time [s]')
#     a1.set_title(
#         "Before Time Alignment", y=title_position)
#     plt.hold("on")

#     min_time = min(np.amin(times_A), np.amin(times_B))
#     times_A_zeroed = times_A - min_time
#     times_B_zeroed = times_B - min_time

#     plt.plot(times_A_zeroed, signal_A, c='r')
#     plt.plot(times_B_zeroed, signal_B, c='b')

#     times_A_shifted = times_A + time_offset

#     a3 = plt.subplot(1, 3, 2)
#     a3.get_xaxis().get_major_formatter().set_useOffset(False)
#     plt.ylabel('correlation')
#     plt.xlabel('sample idx offset')
#     a3.set_title(
#         "Correlation Result \n[Ideally has a single dominant peak.]",
#         y=title_position)
#     plt.hold("on")
#     plt.plot(np.arange(-len(signal_A) + 1, len(signal_B)), convoluted_signals)

#     a2 = plt.subplot(1, 3, 3)
#     a2.get_xaxis().get_major_formatter().set_useOffset(False)
#     plt.ylabel('angular velocity norm [rad]')
#     plt.xlabel('time [s]')
#     a2.set_title(
#         "After Time Alignment", y=title_position)
#     plt.hold("on")
#     min_time = min(np.amin(times_A_shifted), np.amin(times_B))
#     times_A_shifted_zeroed = times_A_shifted - min_time
#     times_B_zeroed = times_B - min_time
#     plt.plot(times_A_shifted_zeroed, signal_A, c='r')
#     plt.plot(times_B_zeroed, signal_B, c='b')

#     plt.subplots_adjust(left=0.04, right=0.99, top=0.8, bottom=0.15)

#     if plt.get_backend() == 'TkAgg':
#         mng = plt.get_current_fig_manager()
#         max_size = mng.window.maxsize()
#         max_size = (max_size[0], max_size[1] * 0.45)
#         mng.resize(*max_size)
#     plt.show(block=block)