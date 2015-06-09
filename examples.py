# -*- coding: utf-8 -*-
# examples on how to use "openweathermapy"

import sys
#from __future__ import print_function
from openweathermapy import get_current_data, get_forecast_data, utils


LOCATION_DEFAULT = "Kassel,DE"

def example1(location):
	# fetch current data with temperatures in C(elsius)
	data = get_current_data(location, units="metric")
	print data

	# get current temperature from nested dictionary
	print utils.get_item(data, "main/temp"), "Celsius"

	# fetch current weather data with temperatures in K(elvin)
	data = get_current_data(location)
	print utils.get_item(data, "main/temp"), "Kelvin"

def example2(location):
	# fetch forcast data with temperatures in C(elsius)
	data = get_forecast_data(location, units="metric")
	print data["list"] 

if __name__ == "__main__":
	print "as first argument you can pass <city>, e. g. 'London,GB'"
	if len(sys.argv) > 1:
		location = sys.argv[1]
	else:
		location = LOCATION_DEFAULT
	#example1(location)
	example2(location)
	
