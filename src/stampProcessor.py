import numpy as np
import matplotlib.pyplot as plt

def removeBeacons(timeStamp, detector):
	# print(detector[0:100])
	for i in range(len(timeStamp) - 1):
		if ((timeStamp[i] == timeStamp[i+1]) or (timeStamp[i] == timeStamp[i-1])):
			print(
				'index:', i,
				'timestamp:', timeStamp[i], 
				'detector:', detector[i]
			)

def removeAnomalies(timeStampBob):
	print("removing anomalies from timestamps")
	# manually remove anomalies in timeStampBob
	# TODO: automate this using standard deviation
	timeStampBob = timeStampBob[0: int( 8.2*len(timeStampBob)/14 )]
	return timeStampBob

def setStart(timeStampAlice, timeStampBob):
	print("setting start of timestamps to 0")

	timeStampAlice = timeStampAlice - min(timeStampAlice)
	timeStampBob = timeStampBob - min(timeStampBob)
	return timeStampAlice, timeStampBob

def findIdxOfTimeStamp(time, timeStamp):
	coeffs = np.polyfit(
		np.linspace(0, len(timeStamp), len(timeStamp)), 
		timeStamp,
		1)
	idx = (time - coeffs[1]) / coeffs[0]
	return int(idx)

def sortArrays(arr1, arr2):
	if (len(arr1) > len(arr2)):
		return arr2, arr1
	else:
		return arr1, arr2

def timebin(tau, timeStamp):

	def bin(arr,t):
		binnedArray = [0]
		arrRange = max(arr) - min(arr)
		maxBinIdx = int(np.ceil(arrRange / t))
		arrIdx = 0

		for binIdx in range(maxBinIdx):
			binLimit = (binIdx)*t
			while (arr[arrIdx] < binLimit and arrIdx < len(arr)):
				binnedArray[binIdx - 1] += 1
				arrIdx += 1
			
			binnedArray.append(0)
			continue

		return list(np.array(binnedArray))

	print("starting to bin timestamp")
	timebin = bin(timeStamp, tau)

	timebin = timebin - np.mean(timebin)

	timebin = timebin[10:]
	return timebin

def plotStamps(timeStampAlice, timeStampBob, timebinAlice, timebinBob, title):

	def plot(data, xlabel, ylabel, title):
		plt.plot(
			data,
			marker = 'o' , 
			markersize = 2,
			# linestyle = "None"
		)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.savefig("../paper/assets/"+title+".png", bbox_inches = 'tight')
		plt.close()

	print("plotting timeStampAlice")
	plt.figure()
	plot(timeStampAlice, "Timestamps", "Event index", title + "TimeStampAlice")

	print("plotting timeStampBob")
	plt.figure()
	plot(timeStampBob, "Timestamps", "Event index", title + "TimeStampBob")

	print("plotting timebinAlice")
	plt.figure()
	plot(timebinAlice, "Timebins", "Events", title + "TimebinAlice")

	print("plotting timebinBob")
	plt.figure()
	plot(timebinBob, "Timebins", "Events", title + "TimebinBob")
