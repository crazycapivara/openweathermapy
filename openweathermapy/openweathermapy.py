# -*- coding: utf-8 -*-
"""
	openweathermapy.openweathermapy
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Core package containing functions to fetch data in `json-format`
	from `OpenWeatherMap.org` and convert it to python types.

	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see <http://www.gnu.org/licenses/gpl.txt> for more details.
"""
import urllib
import json
import utils

# q=<city,country> (e. g. "Kassel,DE"), units can be "standard" or "metric"
URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather?q=%s&units=%s"
URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast?q=%s&units=%"

def get_owm_data(location, url=URL_CURRENT, units="standard"):
	io_stream = urllib.urlopen(url %(location, units))
	data = io_stream.read()
	io_stream.close()
	return json.loads(data)
