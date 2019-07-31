import numpy as np
import matplotlib.pyplot as plt


class DopplerShift:

	def __init__(
		self,
		timeStamp,
		delay,

		nt_list,
		delay_list,
		df_list
	):
		self.timeStamp = timeStamp
		self.delay = delay
		self.shiftedTimeStamp = None

		self.nt_list = nt_list
		self.delay_list = delay_list
		self.df_list = df_list

	def firstOrderDopplerShift(self):
		coeffs = np.polyfit(self.nt_list, self.delay_list, 2)
		print('first order coeffs', coeffs)
		self.shiftedTimeStamp = self.timeStamp.copy()

		for i in range(len(self.timeStamp)):
			t = self.shiftedTimeStamp[i]
			self.shiftedTimeStamp[i] =  t + (coeffs[0]*t*t + coeffs[1]*t + coeffs[2]) 

	def secondOrderDopplerShift(self):
		coeffs = np.polyfit(self.nt_list, self.df_list, 3)
		print('second order coeffs', coeffs)
		for i in range(len(self.timeStamp)):
			t = self.timeStamp[i]
			self.shiftedTimeStamp[i] =  self.shiftedTimeStamp[i] + t*(coeffs[0]*t*t*t + coeffs[1]*t*t + coeffs[2]*t + coeffs[3]) 

	def offset(self):
		self.shiftedTimeStamp = self.shiftedTimeStamp[self.delay:].copy()

	def plotDopplerShift(self):
		print("plotting Doppler shifted signal")
		plt.figure()
		plt.plot(self.shiftedTimeStamp)
		plt.savefig("../paper/assets/doppler_shifted.png") 
		plt.close()

	def shift(self):
		self.firstOrderDopplerShift()
		self.secondOrderDopplerShift()
		self.offset()
		self.plotDopplerShift()
