# -*- coding: utf-8 -*-
"""
	openweathermapy.openweathermapy
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Core module containing functions and classes to fetch data in `json-format`
	from `OpenWeatherMap.org` and convert it to python types.

	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see <http://www.gnu.org/licenses/gpl.txt> for more details.
"""
import urllib
import json
import utils

# q=<city,country> (e. g. "Kassel,DE"), units can be "standard" or "metric"
URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather?q=%s&units=%s"
URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast?q=%s&units=%s"

def get_owm_data(url):
	"""Return nested (data) dictionary for query (url)."""
	io_stream = urllib.urlopen(url)
	data = io_stream.read()
	io_stream.close()
	return json.loads(data)

def wrapper_get_owm_data(func):
	def inner(*args, **kwargs):
		url = func(*args, **kwargs)
		return get_owm_data(url)
	return inner

@wrapper_get_owm_data
def get_current_data(location, units="standard"):
	url = URL_CURRENT %(location, units)
	return url

@wrapper_get_owm_data
def get_forecast_data(location, units="standard"):
	url = URL_FORECAST %(location, units)
	return url

class OpenWeatherMapy(object):
	def __init__(self, data):
		self.data = data

	def get(self, key):
		return utils.get_item(self.data, key)

	def get_many(self, keys):
		items = utils.get_many(self.data, keys)
		return items

class ForecastData(OpenWeatherMapy):
	def __call__(self, keys=None):
		for line in self.data["list"]:
			if keys:
				line = utils.get_many(line, keys)
			yield line

	def fetch_all(self, keys=None):
		data = [line for line in self(keys)]
		return data

