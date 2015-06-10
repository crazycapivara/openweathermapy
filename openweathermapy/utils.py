# -*- coding: utf-8 -*-
"""
	openweathermapy.utils
	~~~~~~~~~~~~~~~~~~~~~
	utility module containing functions to load settings from
	`json-file(s)` and to get items from `nested dictionary` as
	returned from `OpenWeatherMap.org`.

	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see <http://www.gnu.org/licenses/gpl.txt> for more details.
"""

import json

__author__ = "Stefan Kuethe"
__license__ = "GPLv3"

def load_config(filename):
	"""Fetch settings from `json-file`.

	:return: dictionary
	"""
	with file(filename) as f:
		data = f.read()
	return json.loads(data)

def __parse_key(key):
	"""Helper function for `get_item`."""
	if key[0] == "[":
		key = int(key.strip("[]"))
	return key

def get_item(data, key, separator="/"):
	"""Get item from nested dictionary.

	:param data: nested dictionary, e. g. ``data={"a": 2, "b": 4, "c": {"d": 6, "e": 8}}``
	:param key: string in the form of <key><separator><key>...,
	            e. g. ``key="c/d"`` will return ``data["c"]["d"]``
	            if you got a list as well, ``key="c/d/[0]"`` will return ``data["c"]["d"][0]``
	"""
	keys = key.split(separator)
	item = data[__parse_key(keys[0])]
	if len(keys) > 1:
		for key in keys[1:]:
			item = item[__parse_key(key)]
	return item

def get_many(data, keys, *args, **kwargs):
	"""Get multiple items from nested dictionary.

	for details see `get_item` method
	"""
	items = [get_item(data, key, *args, **kwargs) for key in keys]
	return tuple(items)

class _nested_dict(dict):
	"""Dictionary, which is browsable like a filesystem."""
	def __call__(self, key):
		if type(key) == list:
			return self.get_many(key)
		return self.get(key)

	def get(self, key):
		return get_item(self, key)

	def get_many(self, keys):
		return get_many(self, keys)


