# -*- coding: utf-8 -*-
# examples on how to use "openweathermapy"

from openweathermapy import get_owm_data, utils

LOCATION = "Kassel,DE"

def example1():
	# fetch current weather data with temperatures in °C
	current_weather_data = get_owm_data(LOCATION, units="metric")
	print current_weather_data

	# get current temperature from nested dictionaries
	print utils.get_item(current_weather_data, "main/temp"), "Celsius"

	# fetch current weather data with temperatures in K
	current_weather_data = get_owm_data(LOCATION)
	print utils.get_item(current_weather_data, "main/temp"), "Kelvin"

if __name__ == "__main__":
	example1()	
