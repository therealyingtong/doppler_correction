import ephem
import matplotlib.pyplot as plt
import numpy as np 

def calcDoppler(self):

	print("calculating Doppler shift")

	s_list = [] # range (range = distance from observer to satellite)
	v_list = [] # range rate of change 
	t_list = [] # time
	timeRange = (max(self.timeStampAlice) - min(self.timeStampAlice)) * self.units
	print('timeRange', timeRange)
	for i in range (int(timeRange) * 10):
		d_time = ephem.Date(self.startTime + (ephem.second * i * 0.1))

		self.loc.date = d_time

		self.sat.compute(self.loc)

		s_list.append(self.sat.range)
		v_list.append(self.sat.range_velocity)
		t_list.append(d_time)

	df_list = []
	delay_list = []
	nt_list = [(t - self.startTime)*24*60*60 for t in t_list]

	for s in s_list:
		delay = s / ephem.c
		delay_list.append(delay)
		
	for v in v_list:
		df = -(v / ephem.c) 
		df_list.append(df)

	self.nt_list = [nt / self.units for nt in nt_list]
	self.df_list = [df * 2e2 for df in df_list]
	self.delay_list = [delay / self.units for delay in delay_list]


def plotDoppler(self):

	print("plotting Doppler shift")

	plt.figure()
	plt.plot(self.nt_list, self.df_list)
	plt.title('Second order Doppler shift')
	plt.xlabel("time (ns)")
	plt.ylabel('second order Doppler shift')
	plt.savefig("../paper/assets/range_velocity.png") 
	plt.close()

	print("plotting Doppler delay")
	plt.figure()
	plt.plot(self.nt_list, self.delay_list)
	plt.title('Delay due to Doppler shift')
	plt.xlabel("time (ns)")
	plt.ylabel('delay (ns)')
	plt.savefig("../paper/assets/delay.png") 
	plt.close()