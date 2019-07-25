import numpy as np
import matplotlib.pyplot as plt

def removeAnomalies(self):
    print("removing anomalies from timestamps")
    # manually remove anomalies in timeStampBob
    # TODO: automate this using standard deviation
    self.timeStampBob = self.timeStampBob[0: int( 8.2*len(self.timeStampBob)/14 )]

def setStart(self):
    print("setting start of timestamps to 0")
    self.timeStampAlice = self.timeStampAlice - min(self.timeStampAlice)
    self.timeStampBob = self.timeStampBob - min(self.timeStampBob)

def timebin(self):

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
	self.timebinAlice = bin(self.timeStampAlice, self.tau)
	print("starting to bin shifted alice timestamps")
	self.shiftedTimebinAlice = bin(self.shiftedTimeStampAlice, self.tau)
	print("starting to bin bob timestamps")
	self.timebinBob = bin(self.timeStampBob, self.tau)

	# trim leading and trailing zeros
	self.timebinAlice = np.trim_zeros(self.timebinAlice)
	self.shiftedTimebinAlice = np.trim_zeros(self.shiftedTimebinAlice)
	self.timebinBob = np.trim_zeros(self.timebinBob) 

	# normalise timebins
	self.timebinAlice = self.timebinAlice - np.mean(self.timebinAlice)
	self.shiftedTimebinAlice = self.shiftedTimebinAlice - np.mean(self.shiftedTimebinAlice)
	self.timebinBob = self.timebinBob - np.mean(self.timebinBob)

	def padFFT(arr1, arr2):

		def findNextPower2(number):
			if number < 1:
				return 1
			else:
				i = 1
				while i < number:
					i = i*2
				return i

		nextPower2 = findNextPower2(max(len(arr1), len(arr1)))
		diffLen1 = nextPower2 - len(arr1)
		diffLen2 = nextPower2 - len(arr2)

		arr1 = np.concatenate([np.zeros(int(np.floor(diffLen1/2))), arr1, np.zeros(int(np.ceil(diffLen1/2)))])
		arr2 = np.concatenate([np.zeros(int(np.floor(diffLen2/2))), arr2, np.zeros(int(np.ceil(diffLen2/2)))])

		return arr1, arr2

	# # pad arrays to same size
	self.timebinAlice, self.timebinBob = padFFT(
		self.timebinAlice, self.timebinBob
	)
	self.timebinAlice, self.shiftedTimebinAlice = padFFT(
		self.timebinAlice, self.shiftedTimebinAlice
	)

	self.timebinAlice = self.timebinAlice[10:]
	self.shiftedTimebinAlice = self.shiftedTimebinAlice[10:]
	self.timebinBob = self.timebinBob[10:]

def plotStamps(self):

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

    print("plotting timeStampAlice")
    plt.figure()
    plot(self.timeStampAlice, "Timestamps", "Event index", "alice")

    print("plotting timeStampBob")
    plt.figure()
    plot(self.timeStampBob, "Timestamps", "Event index", "bob")

    print("plotting timebinAlice")
    plt.figure()
    plot(self.timebinAlice, "Timebins", "Events", "alice_bin")

    print("plotting shiftedTimeBinAlice")
    plt.figure()
    plot(self.shiftedTimebinAlice, "Timebins", "Events", "alice_shift_bin")

    print("plotting timebinBob")
    plt.figure()
    plot(self.timebinBob, "Timebins", "Events", "bob_bin")
