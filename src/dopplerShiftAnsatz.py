import numpy as np
import ephem
import astropy as astro
import matplotlib.pyplot as plt
import scipy.constants as constants

def calcDoppler(sat, loc, startTime, timeStamp, units):

	print("calculating Doppler shift")

	s_list = [] # range (range = distance from observer to satellite)
	v_list = [] # range rate of change 
	t_list = [] # time
	timeRange = (max(timeStamp) - min(timeStamp)) * units
	print('timeRange', timeRange, 's')
	# for i in range (int(timeRange) * int(1e3)):
	for i in range (int(timeRange) * int(1e5)):

		# d_time = ephem.Date(startTime + (ephem.second * i * 1e-3))
		d_time = ephem.Date(startTime + (ephem.second * i * 1e-5))

		loc.date = d_time

		sat.compute(loc)

		s_list.append(sat.range)
		v_list.append(sat.range_velocity)
		t_list.append(d_time)

	df_list = []
	delay_list = []
	nt_list = [(t - startTime)*24*60*60 for t in t_list]

	for s in s_list:
		delay = s / constants.c
		delay_list.append(delay)
		
	for v in v_list:
		df = - v / constants.c
		df_list.append(df)

	nt_list = [nt / units for nt in nt_list]
	delay_list = [delay / units for delay in delay_list]
	df_list = [df * 2e2 for df in df_list]

	return nt_list, delay_list, df_list

def unshiftPropagationDelay(timeStamp, nt_list, delay_list, deg):
	coeffs = np.polyfit(nt_list, delay_list, deg)
	print('propagationDelay coeffs', coeffs)
	unshiftedTimeStamp = timeStamp.copy()
	coeffsFlipped = np.flip(coeffs)

	for i in range(len(timeStamp)):
		t = unshiftedTimeStamp[i]
		shift = 0
		for j in range(len(coeffsFlipped) - 1, -1, -1):
			shift = shift + coeffsFlipped[j]*(t**j)
		unshiftedTimeStamp[i] =  t - shift

	return unshiftedTimeStamp, coeffs

def plotDoppler(nt_list, df_list, delay_list):

	print("plotting Doppler shift")

	plt.figure()
	plt.plot(nt_list, df_list)
	plt.title('Second order Doppler shift')
	plt.xlabel("time (ns)")
	plt.ylabel('second order Doppler shift')
	plt.savefig("../paper/assets/range_velocity.png") 
	plt.close()

	print("plotting Doppler delay")
	plt.figure()
	plt.plot(nt_list, delay_list)
	plt.title('Delay due to Doppler shift')
	plt.xlabel("time (ns)")
	plt.ylabel('delay (ns)')
	plt.savefig("../paper/assets/delay.png") 
	plt.close()