import numpy as np

class DopplerShift:

	def __init__(
		self,
		timeStamp,
		clockOffset,
		clockDrift,
		tau,
		units,

		nt_list,
		delay_list,
		df_list
	):
		self.timeStamp = timeStamp
		self.clockOffset = clockOffset
		self.clockDrift = clockDrift
		self.tau = tau
		self.units = units

		self.shiftedTimeStamp = None
		self.shiftedTimebin = []

		self.nt_list = nt_list
		self.delay_list = delay_list
		self.df_list = df_list

	def propagationDelay(self):
		coeffs = np.polyfit(self.nt_list, self.delay_list, 2)
		print('first order coeffs', coeffs)
		self.shiftedTimeStamp = self.timeStamp.copy()

		for i in range(len(self.timeStamp)):
			t = self.shiftedTimeStamp[i]
			self.shiftedTimeStamp[i] =  t + (coeffs[0]*t*t + coeffs[1]*t + coeffs[2]) + self.clockOffset

	def clockDriftShift(self):
		coeffs = np.polyfit(
			self.nt_list, self.df_list, 3
		)
		print('second order coeffs', coeffs)
		for i in range(len(self.shiftedTimeStamp)):
			t = self.shiftedTimeStamp[i] 
			drift = self.clockDrift
			secondOrderShift = t*(drift + (coeffs[0]*t*t*t + coeffs[1]*t*t + coeffs[2]*t + coeffs[3]))
			self.shiftedTimeStamp[i] = t + secondOrderShift

	def offset(self):
		self.shiftedTimeStamp = self.shiftedTimeStamp[self.clockOffset:].copy()


