# -*- coding: utf-8 -*-
"""
	openweathermapy.openweathermapy
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Core module containing functions and classes to fetch data in `json-format`
	from `OpenWeatherMap.org` and convert it to python types.
	Items of returned data (mostly nested dictionaries) can be accessed in the way
	you browse your filesystem:

	`item = data("main/temp")` equals `item = data["main"]["temp"]`

	Multiple items can be fetched at once by passing a list of keys:

	`items = data(["main/temp", "wind/speed"])`

	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see <http://www.gnu.org/licenses/gpl.txt> for more details.
"""
import urllib
import json
import utils

UNITS = "standard"
LANGUAGE = "en"

# ("Kassel,DE", "Malaga,ES", "New York,US")
CITIES = (2892518, 2514256, 5128581)

KASSEL_LATITUDE = 51.32
KASSEL_LONGITUDE = 9.5

BASE_URL="http://api.openweathermap.org/data/2.5/"
# q=<city,country> (e. g. "Kassel,DE"), units can be "standard" or "metric"
URL_CURRENT = BASE_URL+"weather?q=%s&units=%s&lang=%s"
URL_CURRENT_ID = BASE_URL+"weather?id=%d&units=%s&lang=%s"
URL_CURRENT_GROUP = BASE_URL+"group?id=%s&units=%s&lang=%s" 
URL_FORECAST = BASE_URL+"forecast?q=%s&units=%s&lang=%s"
URL_FORECAST_ID = BASE_URL+"forecast?id=%s&units=%s&lang=%s"
# lat=<latitude>, lon=<longitude>, cnt=<number of stations>
URL_SEARCH_STATIONS = BASE_URL+"station/find?lat=%d&lon=%d&cnt=%d"

URL_ICON = "http://openweathermap.org/img/w/%s.png" 

URL_CITY_LIST = "http://openweathermap.org/help/city_list.txt"

def get_owm_data(url):
	"""Return data as (nested) dictionary for given `url` request."""
	#io_stream = urllib.urlopen(url)
	#data = io_stream.read()
	#io_stream.close()
	data = utils.get_url_response(url)
	return json.loads(data)

# do not fetch complete list in any case!?
"""
def search_city(city):
	io_stream = urllib.urlopen(URL_CITY_LIST)
	data = [line for line in io_stream if line.find(city) == 0]
	io_stream.close()
	return data
"""

# should search more than one city at once... if wanted!
# save_city_list would be nice for faster search access afterwards
# maybe it should be returned as MemoryFile!? 
def get_city_list(filename=None, search_city=None):
	if filename:
		with file(filename) as f:
			data = f.read().splitlines()
	else:
		data = utils.get_url_response(URL_CITY_LIST).splitlines()
	data = [tuple(line.split("\t")) for line in data]
	if search_city:
		data = [line for line in data if line[1].find(search_city) == 0]
	return data

# key should be icon, data is not needed!
def get_icon_url(icon_name):
		return URL_ICON %icon_name

# obsolete, use wrapper class instead!
def wrapper_get_owm_data(func):
	def inner(*args, **kwargs):
		url = func(*args, **kwargs)
		return get_owm_data(url)
	return inner

class wrapper(object):
	"""Wrapper class for decorators in order to fetch owm data."""
	def __init__(self, func):
		self.func = func
	
	def __call__(self, *args, **kwargs):
		"""my doc here."""
		# rename data_class to data_wrapper because it can be a function as well
		url, data_class = self.func(*args, **kwargs)
		return data_class(get_owm_data(url))

# there should be a method returning "icon-url"
# maybe class should be renamed to weatherData? because forecast list also needs get icon_url,
# or use a method outside class to parse icon into url!?
class CurrentData(utils.nested_dict):
	# not needed!
	def get_icon_url(self):
		icon = self("weather/[0]/icon")
		return URL_ICON % icon

	def _test(self, *keys):
		"""Only for testing purposes, can be deleted!"""
		if len(keys) == 1:
			return self.get(keys[0])
		return self.get_many(keys)

# should use new class `NestedDictList`! obsolete, use new one!
class ForecastData_obs(utils.nested_dict):
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

# any class containing a list with weather data!?
def split_data(data):
	"""Extract list containing weather data from dictionary
	   and return tuple in the form of `(meta_data, weather_data_list)`.
	"""
	list_ = utils.NestedDictList(data.pop("list"))
	meta_data = utils.NestedDict(data)
	return (meta_data, list_)

class ForecastData(utils.NestedDict):
	def iter_list(self, keys=None):
		for line in self["list"]:
			# should be current_weather_data class here, so that get_icon_url can be used!?
			line = utils.NestedDict(line)
			if keys:
				line = line(keys)
			yield line

	# use "self.iter_list" method, because of memory usage!
	def get_list(self, keys=None):
		data = utils.NestedDictList(self["list"])
		if keys:
			data = data.select(keys)
		return data

class CurrentDataGroup(ForecastData):
	pass

# not used anymore, only needed, if Station class should get some extra methods!?
class StationData(list):
	def __init__(self, data):
		list.__init__(self, [Station(line) for line in data])

	# other method than __call__ should be used for this stuff!?
	def __call__(self, keys):
		return [station.get_many(keys) for station in self]

class Station(utils.nested_dict):
	pass

@wrapper
def get_current_data(location, units=UNITS, language=LANGUAGE):
	"""Here comes the doc string, will this one be displayed? or the one from the wrapper?"""
	#maybe another wrapper is needed for get_by_id or by_coord!?
	if type(location) == int:
		_url = URL_CURRENT_ID
	elif type(location) == tuple:
		pass
	else:
		_url = URL_CURRENT
	url = _url %(location, units, language)
	#return (url, CurrentData)
	return (url, utils.NestedDict)
	#return get_owm_data(url)

@wrapper
def get_current_data_group(ids, units="standard", language="en"):
	url = URL_CURRENT_GROUP %(",".join([str(id) for id in ids]), units, language)
	#return (url, utils.NestedDictList)
	#return (url, CurrentDataGroup)
	return (url, split_data)

@wrapper
def get_forecast_data(location, units="standard", language="en"):
	url = URL_FORECAST %(location, units, language)
	#return (url, ForecastData)
	return (url, split_data)

@wrapper
def get_stations(latidude, longitude, count=10):
	url = URL_SEARCH_STATIONS %(latidude, longitude, count)
	#return (url, StationData)
	return (url, utils.NestedDictList)

