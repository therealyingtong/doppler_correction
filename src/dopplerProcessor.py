import ephem
import matplotlib.pyplot as plt
import numpy as np 

def calcDoppler(self):

	print("calculating Doppler shift")

	s_list = [] # range (range = distance from observer to satellite)
	v_list = [] # range rate of change 
	t_list = [] # time
	alt_list = [] # altitude above horizon
	timeRange = (max(self.timeStampAlice) - min(self.timeStampAlice)) * self.units
	print('timeRange', timeRange)
	for i in range (int(timeRange) * 10):
		d_time = ephem.Date(self.startTime + (ephem.second * i * 0.1))

		self.loc.date = d_time

		self.sat.compute(self.loc)

		s_list.append(self.sat.range)
		v_list.append(self.sat.range_velocity)
		t_list.append(d_time)
		alt_list.append(self.sat.alt) 

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
	self.df_list = df_list
	self.delay_list = [delay / self.units for delay in delay_list]

def shiftDoppler(self):
	coeffs = np.polyfit(self.nt_list, self.delay_list, 2)
	print('coeffs', coeffs)
	shiftedTimeStampAlice = []
	for t in self.timeStampAlice:
		shiftedTimeStampAlice.append(
			t + (coeffs[0]*t*t + coeffs[1]*t + coeffs[2]) 
		)

	self.shiftedTimeStampAlice = shiftedTimeStampAlice

def plotDoppler(self):

	print("plotting Doppler shift")

	plt.figure()
	plt.plot(self.nt_list,[df / max(self.df_list) for df in self.df_list])
	plt.title('Doppler shift of ' + str(self.f) + 'Hz clock')
	plt.xlabel("time (seconds)")
	plt.ylabel('Frequency shift in Hz')
	plt.savefig("../paper/assets/range_velocity.png") 


	print("plotting Doppler delay")
	plt.figure()
	plt.plot(self.nt_list, self.delay_list)
	plt.title('Delay due to Doppler shift')
	plt.xlabel("time (ns)")
	plt.ylabel('delay (ns)')
	plt.savefig("../paper/assets/delay.png") 

	print("plotting shifted timestamps for Alice")
	plt.figure()
	plt.plot(self.shiftedTimeStampAlice)
	plt.title('shifted timestamp Alice')
	plt.xlabel("timestamp index")
	plt.ylabel('time (ns)')
	plt.savefig("../paper/assets/alice_shift.png") 