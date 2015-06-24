# openweathermapy
Python package wrapping *OpenWeatherMap.org's* API 2.5.

As *OpenWeatherMap.org* returns data mostly in the form of nested dictionaries,
*openweathermapy* gives a simple API to access items in a comfortable way.
```Python
# classic access
item = data["main"]["temp"]

# openweathermapy access
item = data("main.temp")
```

# Status
Development

# Installation
At the moment just copy *openweathermapy folder* to your python *site-packages folder* or into your *project folder*.

*setup.py* will be added ... soon

# Notes

See TODO and CHANGELOG (not added yet).

# Version
0.5.0

# Usage
```Python
import openweathermapy.core as owm

# fetch current (weather) data
location = "London,GB"
data = owm.get_current(location, units="metric")

# access items
print(data("main.temp"))

[OUT]:
11.06

# fetch multiple items at once
keys = ["main.temp", "main.humidity", "wind.speed"]
print(data.get_many(keys))

[OUT]:
(11.06, 58, 6.2)

# if you like one liners ...
data = owm.get_current("Kassel,DE", units="metric").get_many(keys)

# fetch forecast data
location = "Kassel,DE"
data = owm.get_forecast_hourly(location, units="metric")

keys = ["dt_txt", "main.temp", "weather.[0].description"]
for line in data(keys)
	print(line)

[OUT]:
(u'2015-06-11 18:00:00', 13.54, u'few clouds')
(u'2015-06-11 21:00:00', 10.21, u'sky is clear')
(u'2015-06-12 00:00:00', 8.65, u'few clouds')
(u'2015-06-12 03:00:00', 9.67, u'broken clouds')
(u'2015-06-12 06:00:00', 14.41, u'light rain')
(u'2015-06-12 09:00:00', 18.44, u'light rain')
(u'2015-06-12 12:00:00', 21.82, u'sky is clear')
(u'2015-06-12 15:00:00', 23.42, u'sky is clear')
(u'2015-06-12 18:00:00', 22.36, u'sky is clear')
[...]

# using config files in `json` format
   # config.json
   {
	"default": ["dt_txt", "main.temp", "weather.[0].description"],
	"minimal": ["dt_txt", "main.temp"]
   }

from openweathermapy import utils

keys = utils.load_config("config.json")["default"]
selection = data(keys)
 
# to be continued ...
```
