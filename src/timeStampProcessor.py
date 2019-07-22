import helper
import numpy as np
import matplotlib.pyplot as plt

class TimeStamps:

    def __init__(self, timeStampAlice, timeStampBob, tau):
        self.timeStampAlice = timeStampAlice
        self.timeStampBob = timeStampBob
        self.tau = tau

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
        print("starting to bin timestamps")
        self.timebinAlice = helper.timebin(self.timeStampAlice, self.tau)
        self.timebinBob = helper.timebin(self.timeStampBob, self.tau)

        # trim leading and trailing zeros
        self.timebinAlice = np.trim_zeros(self.timebinAlice)
        self.timebinBob = np.trim_zeros(self.timebinBob) 

        # normalise timebins
        self.timebinAlice = self.timebinAlice - np.mean(self.timebinAlice)
        self.timebinBob = self.timebinBob - np.mean(self.timebinBob)

        # # pad arrays to same size
        self.timebinAlice, self.timebinBob = helper.padFFT(
            self.timebinAlice, self.timebinBob
        )

        self.timebinAlice = self.timebinAlice[10:]
        self.timebinBob = self.timebinBob[10:]

    def processStamp(self):
        print("starting to process timeStamps")
        self.removeAnomalies()
        self.setStart()
        self.timebin()
        print("finished processing timeStamps")

    def plotAll(self):

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
        plt.figure(0)
        plot(self.timeStampAlice, "Timestamps", "Events", "alice")

        print("plotting timeStampBob")
        plt.figure(1)
        plot(self.timeStampBob, "Timestamps", "Events", "bob")

        print("plotting timebinAlice")
        plt.figure(2)
        plot(self.timebinAlice, "Timebins", "Events", "alice_bin")
        
        print("plotting timebinBob")
        plt.figure(3)
        plot(self.timebinBob, "Timebins", "Events", "bob_bin")
