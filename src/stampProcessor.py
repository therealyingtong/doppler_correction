import numpy as np
import matplotlib.pyplot as plt

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

def timebin(tau, timeStamp1, timeStamp2):

	def bin(arr,t):
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

	print("starting to bin timestamps")

	print("starting to bin alice timestamps")
	timebinAlice = bin(timeStamp1, tau)
	print("starting to bin bob timestamps")
	timebinBob = bin(timeStamp2, tau)

	# trim leading and trailing zeros
	timebinAlice = np.trim_zeros(timebinAlice)
	timebinBob = np.trim_zeros(timebinBob) 

	# normalise timebins
	timebinAlice = timebinAlice - np.mean(timebinAlice)
	timebinBob = timebinBob - np.mean(timebinBob)

	def padFFT(arr1, arr2):
		# # arr1 should be longer array
		# if (len(arr1) < len(arr2)):
		# 	copy = arr2.copy()
		# 	arr2 = arr1.copy()
		# 	arr1 = copy

		def findNextPower2(number):
			if number < 1:
				return 1
			else:
				i = 1
				while i < number:
					i = i*2
				return i

		nextPower2 = findNextPower2(max(len(arr1), len(arr2)))
		diffLen1 = nextPower2 - len(arr1)
		diffLen2 = nextPower2 - len(arr2)

		arr1 = np.concatenate([np.zeros(int(np.floor(diffLen1/2))), arr1, np.zeros(int(np.ceil(diffLen1/2)))])
		arr2 = np.concatenate([np.zeros(int(np.floor(diffLen2/2))), arr2, np.zeros(int(np.ceil(diffLen2/2)))])

		return arr1, arr2

	# # pad arrays to same size
	timebinAlice, timebinBob = padFFT(
		timebinAlice, timebinBob
	)
	timebinAlice = timebinAlice[10:]
	timebinBob = timebinBob[10:]
	return timebinAlice, timebinBob

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
