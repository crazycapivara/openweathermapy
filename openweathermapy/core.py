# -*- coding: utf-8 -*-
"""
	openweathermapy.core
	~~~~~~~~~~~~~~~~~~~~
	The core module contains functions and classes to fetch and handle data from
	*OpenWeatherMap.org*. It wraps API 2.5. Items of returned data (mostly nested
	dictionaries) can be accessed in a simplified and flexible way:
	
	   # classic access
	   >>> item = data["main"]["temp"]
	
	   # openweathermapy access
	   >>> item = data("main.temp")
		
	   # access multiple items at once
	   >>> items = data("main.temp", "wind.speed")
	
	Base functions and classes to handle nested dictionaries are located
	in the module ``openweathermapy.utils``.
	
	For a complete list of parameters, which can be passed to the functions
	in this module in the form of keyword arguments (``**params``),
	refer to the API documentation on *http://openweathermap.org*.
	The query string always depends on the request (API call), but unsupported parameters
	will (normally) not raise an error. Most common ones to be used are ``units``,
	``lang`` and (if needed) ``APPID``. So, it may be a good idea to pass them
	as a settings dictionary:
	
	   >>> settings = {"units": "metric", "lang": "DE"}
	   >>> data = get_current("Kassel,DE", **settings)
	   >>> data_in_the_future = get_forecast_daily("Kassel,DE", **settings)
	
	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see <http://www.gnu.org/licenses/gpl.txt> for more details.
"""
import functools
import json
from datetime import datetime
from . import utils

__author__ = "Stefan Kuethe"
__license__ = "GPLv3"

# For testing purposes: ("Kassel,DE", "Malaga,ES", "New York,US")
CITY_IDS = (2892518, 2514256, 5128581)

# For testing purposes: Geographic coordinates for "Kassel,DE"
KASSEL_LATITUDE = 51.32
KASSEL_LONGITUDE = 9.5
KASSEL_LOC = (KASSEL_LATITUDE, KASSEL_LONGITUDE)

BASE_URL = "http://api.openweathermap.org/data/2.5/"
ICON_URL = "http://openweathermap.org/img/w/%s.png" 

CONV = {
	"dt": lambda timestamp: str(datetime.fromtimestamp(timestamp)),
	"weather.[0].icon": lambda icon: ICON_URL % icon
}

def get(url, **params):
	"""Return data as (nested) dictionary for ``url`` request."""
	data = utils.get_url_response(url, **params)
	# Decoding: Python3 compatibility
	return json.loads(data.decode("utf-8"))

# Maybe it would be better and more pythonic to use a class instead of a nested function!?
def wrap_get(appendix, settings=None, converter=None):
	"""Wrap function ``get`` by setting url to ``BASE_URL+appendix``.
	
	Optional args:
	   settings: dictionary with parameters, which will be added to the url request
	      as query string
	   converter: function or class, which will be applied to data
	      returned by the wrapped function
		
	Return:
	   function ``def call(loc=None, **params)``
	
	   Args (of wrapped function):
	      loc (str, int or tuple): name, id or geographic coordinates
	      **params: parameters of query string 
	
	Examples:
	   >>> f = wrap_get("weather", dict(units="metric"))
	   >>> data = f("Kassel,de")
	   >>> data_de = f("Kassel,de", lang="de")
	"""
	url = BASE_URL+appendix
	def call(loc=None, **params):
		if loc:
			if type(loc) == int:
				params["id"] = loc
			elif type(loc) == tuple:
				params.update({"lat": loc[0], "lon": loc[1]})
			else:
				params["q"] = loc
		if settings:
			params.update(settings)
		data = get(url, **params)
		if converter:
			data = converter(data)
		return data
	return call

class GetDecorator(object):
	"""Decorator based on function ``wrap_get``.

	Gives same functionality as function ``wrap_get``,
	except that it is *real* decorator!
	"""
	def __init__(self, appendix, settings=None, converter=None):
		self.get = wrap_get(appendix, settings, converter)

	def __call__(self, f):
		@functools.wraps(f)
		def call(*args, **kwargs):
			params = f(*args, **kwargs)
			data = self.get(**params)
			return data
		return call

class _DataPoint(utils.NestedDict):
	pass

DataPoint = utils.NestedDict

class DataBlock(utils.NestedDictList):
	"""Class for all owm responses containing a list with weather data."""
	def __init__(self, data):
		utils.NestedDictList.__init__(self, data.pop("list"))
		self.meta = utils.NestedDict(data)

def get_current(city=None, **params):
	"""Get current weather data for ``city``.
	
	Args:
	   city (str, int or tuple): name, id
	      or geographic coordinates (latidude, longitude)
	   **params: units, lang[, zip]
	
	Examples:
	   # get data by city name and country code
	   >>> data = get_current("Kassel,DE")
	
	   # get data by city id and set language to german (de)
	   >>> data = get_current(2892518, lang="DE")
	
	   # get data by latitude and longitude and return temperatures in Celcius
	   >>> location = (51.32, 9.5)
	   >>> data = get_current(location, units="metric")
	
	   # optional: skip city argument and get data by zip code
	   >>> data = get_current(zip="34128,DE") 
	"""
	data = wrap_get("weather")(city, **params)
	return DataPoint(data)

def get_current_for_group(city_ids, **params):
	"""Get current weather data for multiple cities.
	
	Args:
	   city_ids (tuple): list of city ids,
	   **params: units, lang
	
	Example:
	   # get data for 'Malaga,ES', 'Kassel,DE', 'New York,US'
	   >>> city_ids = (2892518, 2514256, 5128581)
	   >>> data = get_current_for_group(city_ids, units="metric")
	"""
	id_str = ",".join([str(id_) for id_ in city_ids])
	params["id"] = id_str 
	data = wrap_get("group")(**params)
	return DataBlock(data)

def find_city(city, **params):
	"""Search for ``city`` and return current weather data for match(es).
	
	Examples:
	   >>> data = find_city("New York")
	   >>> data = find_city("Malaga,ES")
	"""
	data = wrap_get("find")(city, **params)
	return DataBlock(data)

# also works with common ``find_city`` function!?
def find_cities_by_geo_coord(geo_coord=None, count=10, **params):
	"""Get current weather data for cities around ``geo_coord``.
	
	Note: Country code is not submitted in response!
	
	Args:
	   geo_coord (tuple): geographic coordinates (latidude, longitude)
	   count (int): number of cities to be returned,
	      defaults to 10
	   **params: units, lang
	"""
	params["cnt"] = count
	data = wrap_get("find")(geo_coord, **params)
	return DataBlock(data)

def get_current_from_station(station_id=None, **params):
	"""Get current weather data from station."""
	data = wrap_get("station")(station_id, **params)
	return DataPoint(data)

def find_stations_by_geo_coord(geo_coord=None, count=10, **params):
	"""Same as ``find cities_by_geo_coord`` but for stations instead of cities."""
	params["cnt"] = count
	data = wrap_get("station/find")(geo_coord, **params)
	return utils.NestedDictList(data)

def get_forecast_hourly(city=None, **params):
	"""Get 3h forecast data for ``city``.
	
	Args:
	   city: see function ``get_current``
	   **params: see *OpenWeatherMap.org's* API for details 
	"""
	data = wrap_get("forecast")(city, **params)
	return DataBlock(data)

def get_forecast_daily(city=None, days=7, **params):
	"""Get daily forcast data for ``city``.
	
	Args:
	   city: see function ``get_current``
	   days: number of days to  be returned, defaults to 7
	   **params: see *OpenWeatherMap.org's* API for details
	"""
	params["cnt"] = days
	data = wrap_get("forecast/daily")(city, **params)
	return DataBlock(data)

def get_history(city=None, **params):
	"""Get historical data for ``city``.
	
	Args:
	   city (str, int or tuple): name, id or
	      geographic coordinates (latidude, longitude)
	   **params: see *OpenWeatherMap.org's* API for details
	"""
	data = wrap_get("history/city")(city, **params)
	return DataBlock(data)

def get_history_from_station(station_id=None, type_="tick", **params):
	"""Get historical data from station.

	If ``type_="tick"`` data is returned in raw format as received
	from the station.
	"""
	params["type"] = type_
	data = wrap_get("history/station")(station_id, **params)
	return DataBlock(data)

# Test of class ``GetDecorator``
@GetDecorator("history/station", None, DataBlock)
def _get_history_from_station(station_id=None, type_="tick", **params):
	"""Get historical data from station."""
	params.update({"id": station_id, "type": type_})
	return params

# Another test of class ``GetDecorator``
@GetDecorator("forecast", dict(units="metric"), DataBlock)
def _get_forecast_hourly(city, **params):
	"""This docstring should be wrapped by functools!"""
	params["loc"] = city
	return params
