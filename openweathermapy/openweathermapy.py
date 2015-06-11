# -*- coding: utf-8 -*-
"""
	openweathermapy.openweathermapy
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Core module containing functions and classes to fetch data in `json-format`
	from `OpenWeatherMap.org` and convert it to python types.
	Items of returned data (mostly nested dictionaries) can be accessed in the way
	you browse your filesystem:

	`item = data("main/temp")` equals `item = data["main"]["temp"]`

	multiple items can be fetched at once by passing a key list:

	`items = data(["main/temp", "wind/speed"])`

	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see <http://www.gnu.org/licenses/gpl.txt> for more details.
"""
import urllib
import json
import utils

KASSEL_LATITUDE = 51.32
KASSEL_LONGITUDE = 9.5


BASE_URL="http://api.openweathermap.org/data/2.5/"
# q=<city,country> (e. g. "Kassel,DE"), units can be "standard" or "metric"
URL_CURRENT = BASE_URL+"weather?q=%s&units=%s"
URL_FORECAST = BASE_URL+"forecast?q=%s&units=%s"
# lat=<latitude>, lon=<longitude>, cnt=<number of stations>
URL_SEARCH_STATIONS = BASE_URL+"station/find?lat=%d&lon=%d&cnt=%d"

def get_owm_data(url):
	"""Return data (nested dictionary) for request."""
	io_stream = urllib.urlopen(url)
	data = io_stream.read()
	io_stream.close()
	return json.loads(data)

# obsolete, use wrapper class instead!
def wrapper_get_owm_data(func):
	def inner(*args, **kwargs):
		url = func(*args, **kwargs)
		return get_owm_data(url)
	return inner

class wrapper(object):
	def __init__(self, func):
		self.func = func

	def __call__(self, *args, **kwargs):
		url, data_class = self.func(*args, **kwargs)
		if not data_class:
			pass	
		return data_class(get_owm_data(url))

class CurrentData(utils.nested_dict):
	def _test(self, *keys):
		if len(keys) == 1:
			return self.get(keys[0])
		return self.get_many(keys)

class ForecastData(utils.nested_dict):
	def iter_list(self, keys=None):
		for line in self["list"]:
			if keys:
				line = utils.get_many(line, keys)
			else:
				line = utils.nested_dict(line)
			yield line

	def get_list(self, keys=None):
		data = [line for line in self.iter_list(keys)]
		return data

class StationData(list):
	def __init__(self, data):
		list.__init__(self, [Station(line) for line in data])

	# other method than __call__ should be used for this stuff!?
	def __call__(self, keys):
		return [station.get_many(keys) for station in self]

class Station(utils.nested_dict):
	pass

@wrapper
def get_current_data(location, units="standard"):
	url = URL_CURRENT %(location, units)
	return (url, CurrentData)

@wrapper
def get_forecast_data(location, units="standard"):
	url = URL_FORECAST %(location, units)
	return (url, ForecastData)

@wrapper
def get_stations(latidude, longitude, count=10):
	url = URL_SEARCH_STATIONS %(latidude, longitude, count)
	return (url, StationData)

