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
Development (Alpha)

# Version
0.6.0

# Usage
**Current weather data**
```Python
>>> import openweathermapy.core as owm

# get data by city name and country code
>>> data = get_current("Kassel,DE")
	
# get data by city id and set language to german (DE)
>>> data = get_current(2892518, lang="DE")
	
# get data by latitude and longitude and return temperatures in Celcius
>>> location = (51.32, 9.5)
>>> data = get_current(location, units="metric")
	
# optional: skip city argument and get data by zip code
>>> data = get_current(zip="34128,DE") 

# access single item
>>> data("main.temp")
11.06

# fetch multiple items at once
>>> keys = ["main.temp", "main.humidity", "wind.speed"]
>>> data.get_many(keys)
(11.06, 58, 6.2)

# get data for 'Malaga,ES', 'Kassel,DE', 'New York,US'
>>> city_ids = (2892518, 2514256, 5128581)
>>> data = get_current_for_group(city_ids, units="metric", lang="DE")
>>> data_malaga = data[0]

# get data for 5 cities around geographic coordinates
>>> location = (51.32, 9.5)
>>> data = find_city_by_geo_coord(location, 5)

# get data from station
>>> data = owm.get_current_from_station(4926)

# find stations (and fetch data) by geographic coordinates
>>> location = (51.32, 9.5)
>>> data = owm.find_stations_by_geo_coord(location)
```
