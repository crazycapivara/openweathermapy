# openweathermapy
Python package wrapping *OpenWeatherMap.org's* API 2.5.

As *OpenWeatherMap.org* returns data mostly in the form of nested dictionaries,
*openweathermapy* gives a simple API to access items in a comfortable way:
```Python
# classic access
item = data["main"]["temp"]

# openweathermapy access
item = data("main.temp")

# access multiple items at once
>>> items = data(["main.temp", "wind.speed"])
```

# Status
Development (Alpha)

# Version
0.6.0

# Usage
All parameters defined in *OpenWeatherMap's* API documentation can be passed to the functions
in *openweathermapy* as keyword arguments ``**params``.
The query string always depends on the request (API call), but unsupported parameters will (normally) not raise an error. Most common ones to be used are ``units``, ``lang`` and (if needed) ``APPID``. So, it may be a good idea to pass them
in the form of a settings dictionary:

```Python
>>> import openweathermapy.core as owm
>>> settings = {"units": "metric", "lang": "DE"}
>>> data = owm.get_current("Kassel,DE", **settings)

# settings containing APIKEY
>>> settings = {"APPID": 1111111111, "units": "metric"}
```

**Current weather data**
```Python
# get data by city name and country code
>>> data = owm.get_current("Kassel,DE")
	
# get data by city id and set language to german (DE)
>>> data = owm.get_current(2892518, lang="DE")
	
# get data by latitude and longitude and return temperatures in Celcius
>>> location = (51.32, 9.5)
>>> data = owm.get_current(location, units="metric")
	
# optional: skip city argument and get data by zip code
>>> data = owm.get_current(zip="34128,DE") 

# access single item
>>> data("main.temp")
11.06

# access multiple items at once
>>> keys = ["main.temp", "main.humidity", "wind.speed"]
>>> data.get_many(keys)
(11.06, 58, 6.2)

# get data for 'Malaga,ES', 'Kassel,DE', 'New York,US'
>>> city_ids = (2892518, 2514256, 5128581)
>>> data = owm.get_current_for_group(city_ids, units="metric", lang="DE")
>>> data_malaga = data[0]

# get data for 5 cities around geographic coordinates
>>> location = (51.32, 9.5)
>>> data = owm.find_cities_by_geo_coord(location, 5)

# get data from station
>>> data = owm.get_current_from_station(4926)

# get stations by geographic coordinates
>>> location = (51.32, 9.5)
>>> data = owm.find_stations_by_geo_coord(location)
```

**Forecast data**

The argument ``city`` can be given as *name*, *id*, *geographic coordinates* or *zip code* as shown
in the examples above.  
```Python
# get 3h forecast data
>>> data = owm.get_forecast_hourly("Kassel,DE", lang="DE")
>>> data.meta
{u'city': {u'country': u'DE', u'population': 0, u'id': 2892518,
u'coord': {u'lat': 51.316669, u'lon': 9.5}, u'name': u'Kassel'},
u'message': 0.0185, u'cod': u'200', u'cnt': 7}

>>> selection = data.select(["dt", "temp.min", "temp.max"])
>>> for line in selection:
...    line 
...
(1436871600, 15.58, 20.98)
(1436958000, 13.18, 22.52)
(1437044400, 14.83, 25.36)
(1437130800, 17.18, 28.19)
(1437217200, 17.49, 26.43)
(1437303600, 12.79, 20.33)
(1437390000, 11.69, 19.93)

# get daily forecast data for 14 days
data = owm.get_forecast_daily("Kassel,DE", 14)
```

**Historical data**

For a complete list of parameters as ``start``, ``end`` etc., which can be passed, please refer
to *OpenWeatherMap's* API documention. 

```Python
# get historical data for city
>>> data = owm.get_history("Kassel,DE")

# get historical data from station
>>> data = owm.get_history_from_station(4926)
```
