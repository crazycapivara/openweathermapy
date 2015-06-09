# -*- coding: utf-8 -*-
"""
	openweathermapy.utils
	~~~~~~~~~~~~~~~~~~~~~
	utility package containing functions to load settings from
	`json-file(s)` and to get get items from `nested dictionaries` as
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

def get_item(data, key, separator="/"):
	"""Get item from nested dictionaries.

	:param data: nested dictionary, e. g. ``data={"a": 2, "b": 4, "c": {"d": 6, "e": 8}}``
	:param key: string in the form of <key><separator><key>...,
	            e. g. ``key="c/d"`` will return ``data["c"]["d"]``
	"""
	keys = key.split(separator)
	item = data[keys[0]]
	if len(keys) > 1:
		for key in keys[1:]:
			item = item[key]
	return item
