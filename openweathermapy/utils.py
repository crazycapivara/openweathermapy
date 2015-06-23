# -*- coding: utf-8 -*-
"""
	openweathermapy.utils
	~~~~~~~~~~~~~~~~~~~~~
	Utility module containing functions and classes to handle nested dictionaries
	(as returned by *OpenWeatherMap.org*) in simplified and flexible way.

	Furthermore, it includes functions to load settings from config file in
	 `json` format and to retrieve data for a given url request.

	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see <http://www.gnu.org/licenses/gpl.txt> for more details.
"""
from __future__ import print_function
import json
# Python3 compatibility (maybe `six` package should be used!?)
try:
	from urllib import urlopen, urlencode
except ImportError:
	from urllib.request import urlopen
	from urllib.parse import urlencode

__author__ = "Stefan Kuethe"
__license__ = "GPLv3"

KEY_SEPARATOR = "."

def get_url_response(url, **params):
	"""Get (raw) data for given `url` and **params."""
	if params:
		url = url+"?"+urlencode(params)
	response = urlopen(url)
	data = response.read()
	response.close()
	return data

def load_config(filename):
	"""Fetch settings from `json` file and return dictionary."""
	with file(filename) as f:
		data = f.read()
	# Decoding: Python3 compatibility
	return json.loads(data.decode("utf-8"))

def __parse_key(key):
	"""Helper function for `get_item`."""
	if key[0] == "[":
		key = int(key.strip("[]"))
	return key

def get_item(data, key):
	"""Get item from nested dictionary in a simplified way.

	Args:
	   data (dict): nested dictionary
	   key (str): request string in the form of <key><separator><key>...

	Examples:
	   # KEY_SEPARATOR = "."
	   >>> data = {"a": 2, "b": 4, "c": {"d": 6, "e": 8}}
	   >>> data("c.d")
	   6
	   # equals
	   >>> data["c"]["d"]
	   6

	   >>> data = {"a": 2, "b": [4, 6]}
	   >>> data("b.[0]")
	   4
	   # equals
	   >>> data["b"][0]
	   4
	"""
	keys = key.split(KEY_SEPARATOR)
	item = data[__parse_key(keys[0])]
	if len(keys) > 1:
		for key in keys[1:]:
			item = item[__parse_key(key)]
	return item

def get_many(data, keys):
	"""Get multiple items from nested dictionary.

	For details see `get_item`.
	"""
	items = [get_item(data, key) for key in keys]
	return tuple(items)

class NestedDict(dict):
	"""Nested dictionary, which is accessible in a simplified way.

	For details see `get_item`.
	"""
	def __call__(self, key):
		if type(key) == list:
			return self.get_many(key)
		return self.get(key)

	def get(self, key):
		"""Get single item."""
		return get_item(self, key)

	def get_many(self, keys):
		"""Get multiple items."""
		return tuple([self.get(key) for key in keys])
		#return get_many(self, keys)

# for old compatibility reasons!?
class nested_dict(NestedDict):
	pass

class NestedDictList(list):
	"""List of (nested) dictionaries (with same keys).

	Example:
	   >>> data = NestedDictList([
	          {"name": "Peter", "nick": "p", "more": {"phone": 888}},
	          {"name": "Jane",  "nick": "j", "more": {"phone": 777}}
	       ])

	   # Extract nick and phone
	   >>> data.select(["nick", "more.phone"])
	   [("p", 888), ("j", 777)]	
	"""

	def __init__(self, data):
		list.__init__(self, [NestedDict(line) for line in data])

	def __call__(self, keys):
		return self.select(keys)

	def select(self, keys):
		selection = [line.get_many(keys) for line in self]
		return selection

