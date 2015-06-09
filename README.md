# openweathermapy
Python package to fetch weather data from `OpenWeatherMap.org`

# Usage
## Current weather data
```Python
>>> from openweathermapy import get_current_data, OpenWeatherMapy
>>> location = "London,GB"

# fetch current weather data
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
(10.5, 58, 6.2)

# to be continued ...
```

## Forecast
```Python
>>> from openweathermapy import get_forecast_data, ForecastData

# to be continued
```
