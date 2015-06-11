# openweathermapy
Python package to fetch weather data from *OpenWeatherMap.org*.

As *OpenWeatherMap.org* returns data mostly as nested dictionaries,
*openweathermapy* allows browsing your data as you browse your filesystem:
```Python
# classic access
item = data["main"]["temp"]

# openweathermapy access (classic access is also possible)
item = data("main/temp")
```

# Status
Development

# Installation
At the moment just copy *openweatherimapy folder* to your python *site-packages folder* or into your *project folder*.

*setup.py* will be added ... soon

# Notes
**2015-06-11:**

Examples will be removed and replaced by new ones as soon as possible, because of some API changes.

# Version
0.1.0

# Usage
```Python
import openweathermapy as owm

# fetch current (weather) data
location = "London,GB"
data = owm.get_current_data(location, units="metric")

# you can access items as you browse your filesystem
print data("main/temp")
[OUT]:
11.06

# if you prefer the classic way, it is also possible
print data["main"]["temp"]
[OUT]:
11.06

# fetch multiple items at once
keys = ["main/temp", "main/humidity", "wind/speed"]
print data.get_many(keys)
[OUT]:
(11.06, 58, 6.2)

# fetch forecast data
location = "Kassel,DE"
data = owm.get_forecast_data(location, units="metric")

selection = ["dt_txt", "main/temp", "weather/[0]/description"]
for line in data.get_list(selection)
	print line
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

# fetch stations by latidude and longitude
stations = owm.get_stations(latitude, longitude, count=10)

for station in stations:
	print station(["station/name", "distance"])

[OUT]:
(u'DH1FR-2', 18.15)
(u'ETHF', 23.729)
(u'Lauterbach', 50.11)
(u'EDVK', 52.481)
(u'Rittershausen', 53.101)
(u'DC5DM-1', 61.607)
(u'Eissen', 64.655)
(u'35625 Reiskirchen', 65.226)
(u'DB0LEN-2', 66.077)
(u'DH5DY-6', 67.692)

# to be continued ...
```
