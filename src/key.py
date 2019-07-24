import sys
sys.path.append('../')

import numpy as np
import stampParser 
import stampProcessor 
import satParser 
import satProcessor
import xcorrProcessor 

class Key:

	def __init__(
		self, 
		filenameAlice, 
		filenameBob, 
		filenameTLE, 
		filenameSavedPass,
		tau,
		f
	):
		self.filenameAlice = filenameAlice
		self.filenameBob = filenameBob
		self.filenameTLE = filenameTLE
		self.filenameSavedPass = filenameSavedPass
		self.tau = tau
		self.f = f

		self.timeStampAlice = None
		self.detectorAlice = None
		self.timeStampBob = None
		self.detectorBob = None

		self.sat = None
		self.loc = None
		self.startTime = None

		self.timebinAlice = None
		self.timebinBob = None
		self.cc = None
		self.shift = None
		self.offset = None

		self.nt_list = None
		self.df_list = None


	def parseSatellite(self):
		self.sat, self.loc, self.startTime = satParser.parseSatellite(
			self.filenameTLE, self.filenameSavedPass
		)

	def calcDoppler(self):
		satProcessor.calcDoppler(self)
		np.save('../data/nt_list', self.nt_list)
		np.save('../data/df_list', self.df_list)

	def plotDoppler(self):
		satProcessor.plotDoppler(self)

	def parseStamp(self):
		self.timeStampAlice, self.detectorAlice = stampParser.parseStamp(
			self.filenameAlice
		)
		np.save('../data/timeStampAlice', self.timeStampAlice)
		np.save('../data/detectorAlice', self.detectorAlice)

		self.timeStampBob, self.detectorBob = stampParser.parseStamp(
			self.filenameBob
		)
		np.save('../data/timeStampBob', self.timeStampBob)
		np.save('../data/detectorBob', self.detectorBob)

	def processStamps(self):
		print("starting to process timeStamps")
		stampProcessor.removeAnomalies(self)
		stampProcessor.setStart(self)
		stampProcessor.timebin(self)
		print("finished processing timeStamps")
		np.save('../data/timebinAlice', self.timebinAlice)
		np.save('../data/timebinBob', self.timebinBob)

	def plotStamps(self):
		stampProcessor.plotStamps(self)

	def xcorr(self):
		xcorrProcessor.xcorr(self)

	def plotXcorr(self):
		xcorrProcessor.plotXcorr(self)

