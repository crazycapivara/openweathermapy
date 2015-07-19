# -*- coding: utf-8 -*-
"""
	openweathermapy.utils
	~~~~~~~~~~~~~~~~~~~~~
	The utility module contains functions and classes to handle nested dictionaries
	(as returned by *OpenWeatherMap.org*) in a simplified and flexible way.
	
	Furthermore, it includes functions to load settings from config files in
	 *json* format and to retrieve data for given url requests.
	
	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see <http://www.gnu.org/licenses/gpl.txt> for more details.
"""
import json
# Python3 compatibility (maybe package ``six`` should be used!?)
try:
	from urllib import urlopen, urlencode
except ImportError:
	from urllib.request import urlopen
	from urllib.parse import urlencode

__author__ = "Stefan Kuethe"
__license__ = "GPLv3"

KEY_SEPARATOR = "."

def get_url_response(url, **params):
	"""Get (raw) data for given ``url``."""
	if params:
		url = url+"?"+urlencode(params)
	response = urlopen(url)
	data = response.read()
	response.close()
	return data

def load_config(filename):
	"""Read settings from *json* file and return dictionary."""
	with open(filename) as f:
		data = f.read()
	# Decoding: Python3 compatibility - NOT NEEDED, raised error!
	#return json.loads(data.decode("utf-8"))
	return json.loads(data)

def get_item(data, key):
	"""Get item from nested dictionary in a simplified way.
	
	Args:
	   data (dict): nested dictionary
	   key (str): request string in the form of <key><separator><key>...
	
	Examples:
	   # KEY_SEPARATOR = "."
	   >>> data = {"a": 2, "b": {"c": 6, "d": 8}}

	   # get data["c"]["d"]
	   >>> get_item(data, "b.c")
	   6

	   >>> data = {"a": 2, "b": [4, 6]}

	   # get data["b"][0]
	   >>> get_item(data, "b.[0]")
	   4
	"""
	def parse_key(key):
		if key[0] == "[":
			key = int(key.strip("[]"))
		return key
	keys = key.split(KEY_SEPARATOR)
	item = data[parse_key(keys[0])]
	if len(keys) > 1:
		for key in keys[1:]:
			item = item[parse_key(key)]
	return item

def get_many(data, keys):
	"""Get multiple items from nested dictionary.
	
	For details see function ``get_item``.
	"""
	items = [get_item(data, key) for key in keys]
	return tuple(items)

class NestedDict(dict):
	"""Nested dictionary, which is accessible in a simplified way.
	
	Example:
	   # KEY_SEPARATOR = "."
	   >>> data = NestedDict({"a": 2, "b": {"c": 4, "d": 6}})
	   >>> data("b.d")
	   6
	   >>> data(["a", "b.c"])
	   (2, 4)
	
	For details see function ``get_item``.
	"""
	def __call__(self, *keys):
		"""Call method ``get`` or ``get_many`` depending on number of ``keys``."""
		if len(keys) == 1:
			return self.get_item(keys[0])
		return self.get_many(keys)

	def get_item(self, key):
		"""Get single item for given ``key``."""
		return get_item(self, key)

	def get_many(self, keys, converters=None):
		"""Get multiple items for given ``keys``."""
		def _get(key):
			item = self.get_item(key)
			if converters:
				conv = converters.get(key)
				if conv:
					item = conv(item)
			return item 
		return tuple([_get(key) for key in keys])

	def get_dict(self, keys, split_keys=False, converters=None):
		"""Same as method ``get_many``, but return type is a dictionary."""
		items = self.get_many(keys, converters)
		if split_keys:
			keys = [key.split(KEY_SEPARATOR)[-1] for key in keys]
		return dict(zip(keys, items))

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
		"""Alias for method ``select``."""
		return self.select(keys)

	def select(self, keys, converters=None):
		"""Return data (table) for selected columns (``keys``)."""
		selection = [line.get_many(keys, converters) for line in self]
		return selection

	def select_dict(self, keys, *args, **kwargs):
		"""*args and **kwargs: see ``NestedDict.get_item``."""
		selection = [line.get_dict(keys, *args, **kwargs) for line in self]
		return selection
