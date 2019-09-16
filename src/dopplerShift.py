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

	for stamp in timeStamp:
		d_time = ephem.Date(startTime + (ephem.second * stamp * units))
		loc.date = d_time

		sat.compute(loc)

		s_list.append(sat.range)
		v_list.append(sat.range_velocity)
		t_list.append(d_time)		

	df_list = []
	delay_list = []

	for s in s_list:
		delay = s / constants.c
		delay_list.append(delay)
		
	for v in v_list:
		df = - v / constants.c
		df_list.append(df)

	delay_list = [delay / units for delay in delay_list]
	df_list = [df * 2e2 for df in df_list]

	return delay_list, df_list

def propagationDelay(timeStamp, delay_list):

	shiftedTimeStamp = timeStamp.copy()

	for i in range(len(timeStamp)):
		shiftedTimeStamp[i] = timeStamp[i] + delay_list[i]

	return shiftedTimeStamp

def clockDriftShift(timeStamp, df_list, clockDrift):

	shiftedTimeStamp = timeStamp.copy()

	for i in range(len(shiftedTimeStamp)):
		t = timeStamp[i] 
		drift = clockDrift
		secondOrderShift = t*(drift + df_list[i])
		shiftedTimeStamp[i] = t + secondOrderShift

	return shiftedTimeStamp

def plotDoppler(timeStamp, df_list, delay_list):

	print("plotting Doppler shift")

	plt.figure()
	plt.plot(timeStamp, df_list)
	plt.title('Second order Doppler shift')
	plt.xlabel("time (ns)")
	plt.ylabel('second order Doppler shift')
	plt.savefig("../paper/assets/range_velocity.png") 
	plt.close()

	print("plotting Doppler delay")
	plt.figure()
	plt.plot(timeStamp, delay_list)
	plt.title('Delay due to Doppler shift')
	plt.xlabel("time (ns)")
	plt.ylabel('delay (ns)')
	plt.savefig("../paper/assets/delay.png") 
	plt.close()