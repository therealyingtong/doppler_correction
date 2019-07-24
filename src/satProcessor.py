import ephem
import matplotlib.pyplot as plt

def calcDoppler(self):

	print("calculating Doppler shift")

	v_list = [] # range rate of change (range = distance from observer to satellite)
	t_list = [] # time
	alt_list = [] # altitude above horizon
	for i in range (700):
		d_time = ephem.Date(self.startTime + (ephem.second * i))

		self.loc.date = d_time

		self.sat.compute(self.loc)

		v_list.append(self.sat.range_velocity)
		t_list.append(d_time)
		alt_list.append(self.sat.alt) 

	df_list = []
	nt_list = [(t - self.startTime)*24*60*60 for t in t_list]
	for v in v_list:
		df = -(v / ephem.c) * self.f
		df_list.append(df)

	plt.figure(7)
	plt.plot(v_list)
	plt.show()

	self.nt_list = nt_list
	self.df_list = df_list

def plotDoppler(self):

	print("plotting Doppler shift")

	plt.figure(6)
	plt.plot(self.nt_list,self.df_list)
	plt.title('Doppler shift of ' + str(self.f) + 'Hz clock')
	plt.xlabel("time (seconds)")
	plt.ylabel('Frequency shift in Hz')
	plt.savefig("../paper/assets/doppler.png") 