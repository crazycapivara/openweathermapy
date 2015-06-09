# openweathermapy
Python package to fetch weather data from `OpenWeatherMap.org`

# Usage
```Python
from openweathermapy import get_current_data, OpenWeatherMapy

location = "London,GB"

# fetch current weather data
data = get_current_data(location, units="metric")
print data["main"]["temp"]
```
