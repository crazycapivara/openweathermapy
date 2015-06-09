# -*- coding: utf-8 -*-
# examples on how to use "openweathermapy"
#-----------------------------------------
#from __future__ import print_function

import openweathermapy as owm
from openweathermapy import utils

LOCATION = "London,GB"
LOCATION = "Kassel,DE"

# get current weather data
data = owm.get_current_data(LOCATION, units="metric")
print data

# get items to be extracted from config file
config = utils.load_config("config/config.json")

data = owm.OpenWeatherMapy(data)
print data.get_many(config["default"])
print data.get_many(config["minimal"])

# get forecast data
forecast = owm.get_forecast_data(LOCATION, units="metric")
forecast = owm.ForecastData(forecast)
selection = forecast.fetch_all(config["forecast"])
#print selection
for line in selection:
	print line
