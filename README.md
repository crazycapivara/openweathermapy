# openweathermapy
Python package to fetch weather data from `OpenWeatherMap.org`

# Usage
```Python
>>> location = "London,GB"

# fetch current weather data
>>> from openweathermapy import get_current_data, OpenWeatherMapy
>>> data = get_current_data(location, units="metric")
>>> print data["main"]["temp"]
11.06

# use utils module for nested dictionaries
>>> from openweathermapy import utils
>>> print utils.get_item(data, "main/temp")
11.06

# select multiple values
>>> items = ["main/temp", "main/humidity", "wind/speed"]
>>> print utils.get_many(data, items)
(11.06, 58, 6.2)

# use OpenWeatherMap object (maybe object should be returned by default!?)
>>> data = OpenWeatherMap(data)
>>> print data.get_many(items)
(11.06, 58, 6.2)

# fetch forecast data
>>> from openweathermapy import get_forecast_data, ForecastData
>>> data = get_forecast_data(location, units="metric")
>>> data = ForecastData(data)

# to be continued
```
