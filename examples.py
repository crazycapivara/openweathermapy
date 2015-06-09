# -*- coding: utf-8 -*-
# examples on how to use "openweathermapy"
#-----------------------------------------
from __future__ import print_function

import sys
from openweathermapy import get_current_data, get_forecast_data, utils
from openweathermapy import OpenWeatherMapy, ForecastData

LOCATION_DEFAULT = "Kassel,DE"

def example1(location):
	# fetch current data with temperatures in C(elsius)
	data = get_current_data(location, units="metric")
	print(data)

	# get current temperature from nested dictionary
	print(utils.get_item(data, "main/temp"), "Celsius")

	# fetch current weather data with temperatures in K(elvin)
	#data = get_current_data(location)
	#print utils.get_item(data, "main/temp"), "Kelvin"

	# use "OpenWeatherMap object"
	data = OpenWeatherMapy(data)
	print(data.get("main/temp"))
	print(data.get_many(["name", "sys/country", "main/temp", "main/temp_max", "main/temp_min"]))

def example2(location):
	# fetch forcast data with temperatures in C(elsius)
	data = get_forecast_data(location, units="metric")
	#print data["list"]
	for line in ForecastData(data)(["dt_txt", "main/temp", "weather/[0]/description"]):
		print(line)
	#extracted = ForecastData(data).fetch_all(["dt_txt", "main/temp", "weather/[0]/description"])
	#print extracted 

if __name__ == "__main__":
	print("as first argument you can pass <city>, e. g. 'London,GB'")
	if len(sys.argv) > 1:
		location = sys.argv[1]
	else:
		location = LOCATION_DEFAULT
	example1(location)
	#example2(location)
	
