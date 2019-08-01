import numpy as np
import matplotlib.pyplot as plt


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

	def firstOrderDopplerShift(self):
		coeffs = np.polyfit(self.nt_list, self.delay_list, 2)
		print('first order coeffs', coeffs)
		self.shiftedTimeStamp = self.timeStamp.copy()

		for i in range(len(self.timeStamp)):
			t = self.shiftedTimeStamp[i]
			self.shiftedTimeStamp[i] =  t + (coeffs[0]*t*t + coeffs[1]*t + coeffs[2]) 

	def secondOrderDopplerShift(self):
		coeffs = np.polyfit(
			self.nt_list, self.df_list, 3
		)
		print('second order coeffs', coeffs)
		for i in range(len(self.shiftedTimeStamp)):
			t = self.shiftedTimeStamp[i] 
			drift = self.clockDrift
			secondOrderShift = t*drift + t*drift*(coeffs[0]*drift*drift*drift + coeffs[1]*drift*drift + coeffs[2]*drift + coeffs[3])
			self.shiftedTimeStamp[i] = t + secondOrderShift
			# print('t', t)
			# print('drift', drift)
			# print('t second order shift', secondOrderShift)
	

	# def secondOrderDopplerShift(self):
	# 	coeffs = np.polyfit(
	# 		[nt / self.tau for nt in self.nt_list], self.df_list, 3
	# 	)
	# 	print('second order coeffs', coeffs)
	# 	for i in range(len(self.shiftedTimebin)):
	# 		count = self.shiftedTimebin[i] 
	# 		drift = self.clockDrift
	# 		self.shiftedTimebin[i] = count*drift*(coeffs[0]*drift*drift*drift + coeffs[1]*drift*drift + coeffs[2]*drift + coeffs[3]) 

	def offset(self):
		self.shiftedTimeStamp = self.shiftedTimeStamp[self.clockOffset:].copy()

	def plotDopplerShift(self):
		print("plotting Doppler shifted signal")
		plt.figure()
		plt.plot(self.shiftedTimeStamp)
		plt.savefig("../paper/assets/doppler_shifted.png") 
		plt.close()

