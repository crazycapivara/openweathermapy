# -*- coding: utf-8 -*-
"""
	openweathermapy.core
	~~~~~~~~~~~~~~~~~~~~
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
import functools
#import urllib # still needed?
import json
from . import utils
from . import wrapper as _wrapper


UNITS = "standard"
LANGUAGE = "en"

# ("Kassel,DE", "Malaga,ES", "New York,US")
CITIES = (2892518, 2514256, 5128581)

KASSEL_LATITUDE = 51.32
KASSEL_LONGITUDE = 9.5

BASE_URL="http://api.openweathermap.org/data/2.5/"
# can all be kicked out!
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

def get(url, **params):
	"""Return data as (nested) dictionary for given `url` (request)."""
	data = utils.get_url_response(url, **params)
	# Decoding: Python3 compatibility
	return json.loads(data.decode("utf-8"))

def wrap_get(appendix):
	url = BASE_URL+appendix
	def call(loc=None, **params):
		if loc:
			params["loc"] = loc
		if params.get("loc"):
			loc = params.pop("loc")
			if type(loc) == int:
				params["id"] = loc
			elif type(loc) == tuple:
				params.update({"lat": loc[0], "lon": loc[1]})
			else:
				params["q"] = loc
		data = get(url, **params)
		return data
	return call

# Only for testing purposes, works fine, but not useful in most cases!?
class get_decorator(object):
	def __init__(self, appendix):
		self._get = wrap_get(appendix)

	def __call__(self, f):
		def inner(*args, **params):
			_params = f(*args, **params)
			return self._get(**_params)
		return inner

# Same as above, but without class!
def decorate_get(appendix):
	_get = wrap_get(appendix)
	def decorate(f):
		@functools.wraps(f)
		def call(*args, **params):
			_params = f(*args, **params)
			data = _get(**_params)
			return data
		return call
	return decorate

get_owm_data = get

def get_current(city=None, **params):
	"""Get current weather data."""
	data = wrap_get("weather")(city, **params)
	return data

def get_current_group(city_ids, **params):
	"""Get current weather data for multiple cities at once."""
	id_ = ",".join([str(id_) for id_ in city_ids])
	params["id"] = id_ 
	data = wrap_get("group")(**params)
	return data

def get_current_station(station_id=None, **params):
	"""Tested. Works fine."""
	data = wrap_get("station")(station_id, **params)
	return data

def get_current_station_box(**params):
	pass

def get_current_station_geo(geo_point=None, **params):
	"""..."""
	data = wrap_get("station/find")(geo_point, **params)
	return data

def get_current_box(**params):
	"""Not tested."""
	data = wrap_get("box/city")(**params)
	return data

# move up!
def get_current_cycle(center_point=None, **params):
	"""Tested. Works fine, but country code is not submitted!"""
	data = wrap_get("find")(center_point, **params)
	return data

def get_forecast(city=None, **params):
	"""Get 3h forecast data."""
	data = wrap_get("forecast")(city, **params)
	return data

def get_forecast_daily(city=None, **params):
	"""Get daily forcast data."""
	data = wrap_get("forecast/daily")(city, **params)
	return data

# ----------------------------------------------------------------

@get_decorator("group")
def get_current_group_test(ids, **params):
	loc = ",".join([str(id) for id in ids])
	params.update({"id": loc})
	return params


# Maybe decorator is nicer and more state of the art!?
# But in this case "data parser function" should also be an argument!?
# Furthermore, `functool.wrap` should be used to parse docstring!
#@get_decorator("forecast")
@decorate_get("forecast")
def get_forecast_test(loc, **params):
	"""This docstring should be wrapped!"""
	params["loc"] = loc
	return params

@get_decorator("station/find")
def get_stations(loc, **params):
	#params.update({"lat": loc[0], "lon": loc[1]})
	params["loc"] = loc
	return params

def search_city(city, **params):
	params.update({"q": city})
	search = wrap_get("find")
	data = search(**params)
	return data

#==========================================

def _parse_city_data(data, search, rdict):
	"""Helper function for `get_cities_...`"""
	data = [tuple(line.split("\t")) for line in data]
	keys = data.pop(0)
	if search:
		data = [line for line in data if line[1].find(search) >= 0]
	if rdict:
		return [dict(zip(keys, line)) for line in data]
	return (keys, data)

def get_cities_from_file(filename, search=None, rdict=False):
	"""Get cities from file."""
	with file(filename) as f:
		data = f.read().splitlines()
	return _parse_city_data(data, search, rdict)
	
 
def get_cities(search=None, rdict=False):
	"""Get cities from url."""
	data = utils.get_url_response(URL_CITY_LIST).splitlines()
	return _parse_city_data(data, search, rdict)

def save_cities(filename):
	"""Get cities form url and save it to given `filename`."""
	data = utils.get_url_response(URL_CITY_LIST).splitlines()
	with file(filename, "w") as f:
		f.write(data)

def get_icon_url(icon_name):
	"""Get icon url for given `icon_name`."""
	return URL_ICON %icon_name

# New: now docstring is wrapped as well
def wrapper_get(func):
	@functools.wraps(func)
	def inner(*args, **kwargs):
		url, parser = func(*args, **kwargs)
		data = get_owm_data(url)
		if parser:
			data = parser(data)
		return parser
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
	hangover = utils.NestedDict(data)
	return (hangover, list_)

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


#@wrapper_get
def _get_current(location, units=UNITS, language=LANGUAGE):
	"""Get current weather data for given `location`."""
	if type(location) == int:
		_url = URL_CURRENT_ID
	elif type(location) == tuple:
		pass
	else:
		_url = URL_CURRENT
	url = _url %(location, units, language)
	#return (url, utils.NestedDict)
	return utils.NestedDict(get(url))

def get_current_test(location, units=UNITS, language=LANGUAGE):
	@_wrapper.TypeWrapperMore(location)
	def get_url(*args):
		return (URL_CURRENT, URL_CURRENT_ID)
	url = get_url(units, language)
	return url

# NEW STYLE!
def current(location, **params):
	params.update({"loc": location})
	@_wrapper.Get(BASE_URL+"weather")
	def get_url():
		return params
	return utils.NestedDict(get(get_url()))

get_current_data = get_current

def forecast(location, **params):
	params.update({"loc": location})
	@_wrapper.Get(BASE_URL+"forecast")
	def get_url():
		return params
	return split_data(get(get_url()))

# Testing only
def forecast_alternative(location, **params):
	params.update({"loc": location})
	wrapper = _wrapper._Get(BASE_URL+"forecast")
	url = wrapper(params)
	return split_data(get(url))

def current_group(ids, **params):
	locations = ",".join([str(id) for id in ids])
	params.update({"id": locations})
	@_wrapper.Get(BASE_URL+"group")
	def get_url():
		return params
	return split_data(get(get_url()))

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
def _get_stations(latidude, longitude, count=10):
	url = URL_SEARCH_STATIONS %(latidude, longitude, count)
	#return (url, StationData)
	return (url, utils.NestedDictList)

