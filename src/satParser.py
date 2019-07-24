import ephem

def parseSatellite(filenameTLE, filenameSavedPass):
	tleFile = open(filenameTLE, "r")
	sat = ephem.readtle(
		tleFile.readline(),
		tleFile.readline(),
		tleFile.readline()
	)
	tleFile.close()

	loc = ephem.Observer()
	savedPassFile = open(filenameSavedPass, "r")
	loc.lat = float(savedPassFile.readline()) * ephem.degree
	loc.lon = float(savedPassFile.readline()) * ephem.degree
	loc.elevation = float(savedPassFile.readline()) 

	startTime = ephem.Date(savedPassFile.readline()) + ephem.second * 75
	savedPassFile.close()

	return sat, loc, startTime