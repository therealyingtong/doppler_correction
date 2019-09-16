import numpy as np

def propagationDelay(timeStamp, nt_list, delay_list):
	coeffs = np.polyfit(nt_list, delay_list, 2)
	print('propagationDelay coeffs', coeffs)
	shiftedTimeStamp = timeStamp.copy()

	for i in range(len(timeStamp)):
		t = shiftedTimeStamp[i]
		shiftedTimeStamp[i] =  t + (coeffs[0]*t*t + coeffs[1]*t + coeffs[2])

	return shiftedTimeStamp, coeffs

def clockDriftShift(timeStamp, nt_list, df_list, clockDrift):
	coeffs = np.polyfit(
		nt_list, df_list, 3
	)
	print('clockDriftShift coeffs', coeffs)
	shiftedTimeStamp = timeStamp.copy()

	for i in range(len(shiftedTimeStamp)):
		t = shiftedTimeStamp[i] 
		drift = clockDrift
		secondOrderShift = t*(drift + (coeffs[0]*t*t*t + coeffs[1]*t*t + coeffs[2]*t + coeffs[3]))
		shiftedTimeStamp[i] = t + secondOrderShift

	return shiftedTimeStamp

