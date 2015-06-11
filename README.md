# openweathermapy
Python package to fetch weather data from *OpenWeatherMap.org*.

As *OpenWeatherMap.org* returns data mostly as nested dictionaries,
*openweathermapy* allows browsing your data as you browse your filesystem:
```Python
# classic access
item = data["main"]["temp"]

# openweathermapy access (classic access is also possible)
item = data["main/temp"]
```

# Status
Development

# Note
**2015-06-11**
examples will be removed and replaced by new ones as soon as possible, because of some API changes

# Version
0.0.1

# Usage
```Python
import openweathermapy import as owm

# fetch current weather data for "London,GB"
location = "London,GB"
data = owm.get_current_data(location, units="metric")

# you can access data as you browse a filesystem
print data("main/temp")
[OUT]:
11.06

# if you prefer the classic way, it is also possible  ...
print data["main"]["temp"]
[OUT]:
11.06

# select multiple values
items = ["main/temp", "main/humidity", "wind/speed"]
print data.get_many(items)
[OUT]:
(11.06, 58, 6.2)

# fetch forecast data
location = "Kassel,DE"
data = owm.get_forecast_data(location, units="metric")
[...]

# to be continued ...
```
