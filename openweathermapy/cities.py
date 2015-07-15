# -*- coding: utf-8 -*-
"""
	openweathermapy.cities
	~~~~~~~~~~~~~~~~~~~~~~
	The cities module contains functions to retrieve information (mostly id,
	latitude and longitude) for cities supported by *OpenWeatherMap.org*.
	You can search for cities by name.	
	
	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see <http://www.gnu.org/licenses/gpl.txt> for more details.
"""
from . import utils

__author__ = "Stefan Kuethe"
__license__ = "GPLv3"

URL_CITY_LIST = "http://openweathermap.org/help/city_list.txt"
"""url, where to fetch current city list"""

class CityData(object):
	"""List of cities.

	City attributes:
	   * id (id),
	   * name (nm),
	   * latitude (lat),
	   * longitude (lon),
	   * country code (countryCode)
	"""
	def __init__(self, data, separator="\t"):
		data = [tuple(line.split(separator)) for line in data.splitlines()]
		self.keys = data.pop(0)
		self.data = data

	def get_keys(self):
		"""Get column names, usually not needed."""
		return self.keys

	def get_data(self):
		"""Get list of all cities, usually not needed."""
		return self.data

	def get(self, city):
		"""Search for ``city`` and return list of matches.
		
		Args:
		   city (str): city must either be city name or comma-separated
		   city name with country code, e. g. `New York` or `New York,US`.
		"""
		try:
			name, country = city.split(",")
		except:
			name, country = city, ""
		data = [line for line in self.data if line[1].find(name) >= 0 and line[-1].find(country.upper()) >= 0]
		return data

	def get_dict(self, city):
		"""Same as ``get`` method, but matches are returned as dictionaries."""
		data = self.get(city)
		data_dict = [dict(zip(self.keys, line)) for line in data]
		return data_dict

def load_cities():
	"""Load city data from *OpenWeatherMap.org* and return ``CityData`` object."""
	data = utils.get_url_response(URL_CITY_LIST)
	return CityData(data)

def load_cities_from_file(filename):
	"""Load city data from file and return ``CityData`` object."""
	with file(filename) as f:
		data = f.read()
	return CityData(data)

def save_cities_to_file(filename):
	"""Fetch city list from *OpenWeatherMap.org* and save it to harddisk."""
	data = utils.get_url_response(URL_CITY_LIST)
	with file(filename, "w") as f:
		f.write(data)

