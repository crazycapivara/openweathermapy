# -*- coding: utf-8 -*-
"""
	openweathermapy.utils
	~~~~~~~~~~~~~~~~~~~~~
	Utility module containing functions to load settings from
	`json-file(s)` and to access items from `nested dictionaries` (as
	returned by `OpenWeatherMap.org`) in the way you browse a filesystem.

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

def get_url_response(url, **params):
	"""Get (raw) data for given `url` (and **params)."""
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
	return json.loads(data.decode("ascii"))

def __parse_key(key):
	"""Helper function for `get_item` function."""
	if key[0] == "[":
		key = int(key.strip("[]"))
	return key

def get_item(data, key, separator="/"):
	"""Get item from nested dictionary in a simplified way.

	Examples:
	   >>> data = {"a": 2, "b": 4, "c": {"d": 6, "e": 8}}
	   >>> data("c/d")
	   6
	   # equals
	   >>> data["c"]["d"]
	   6

	   >>> data = {"a": 2, "b": [4, 6]}
	   >>> data("b/[0]")
	   4
	   # equals
	   >>> data["b"][0]
	   4

	:param data: nested dictionary
	:param key: string in the form of <key><separator><key>...
	"""
	keys = key.split(separator)
	item = data[__parse_key(keys[0])]
	if len(keys) > 1:
		for key in keys[1:]:
			item = item[__parse_key(key)]
	return item

def get_many(data, keys, *args, **kwargs):
	"""Get multiple items from nested dictionary.

	For details see `get_item` method.
	"""
	items = [get_item(data, key, *args, **kwargs) for key in keys]
	return tuple(items)

# should be renamed to NestedDict!?
class nested_dict(dict):
	"""Dictionary, which is accessible like a filesystem.

	For example `data("main/name")` equals `data["main"]["name"]`.

	For details see `utils.get_item` method.
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

class NestedDict(nested_dict):
	pass

class NestedDictList(list):
	"""List of (nested) dictionaries (with same keys).

	Example:
	   >>> data = NestedDictList(
	        [{"name": "Peter", "nick": "p", "more": {"phone": 888}},
	          {"name": "Jane",  "nick": "j", "more": {"phone": 777}}]
	       )

	   # Extract nick and phone
	   >>> data.select(["nick", "more/phone"])
	   [("p", 888), ("j", 777)]	
	"""

	def __init__(self, data):
		list.__init__(self, [NestedDict(line) for line in data])

	def __call__(self, keys):
		return self.select(keys)

	def select(self, keys):
		selection = [line.get_many(keys) for line in self]
		return selection

