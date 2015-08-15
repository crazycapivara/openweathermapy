# Openweathermapy
Python package wrapping **OpenWeatherMap.org's** API 2.5.

***

# Overview
As **OpenWeatherMap.org** returns data mostly in the form of nested dictionaries,
**Openweathermapy** gives a simple API to access items in a comfortable way:
```python
# classic access
item = data["main"]["temp"]

# openweathermapy access
item = data("main.temp")

# access multiple items at once
>>> items = data("main.temp", "wind.speed")
```

***

# Status
Development Beta

***

# Version
0.7.0

***

# Changelog
* **2015-08-09** optional ``pandas.DataFrame`` support added for forecast and historical data

***

# Requirements
**Openweathermapy** supports Python 2.7, 3.2, 3.3 and 3.4. There are no more requirements,
but for forecast and historical data ``pandas.DataFrame`` objects can be returned.
So it is cool to install **Pandas** as well but it is not madatory. 

***

# Installation
```bash
# via pip
~$ pip install openweathermapy

# or download package and run ...
~$ python setup.py install
```

***

# Getting started
```Python
>>> import openweathermapy.core as owm
```

All parameters defined in **OpenWeatherMap.org's** API documentation can be passed to the functions
in **Openweathermapy** as keyword arguments ``**params``.
The query string always depends on the request (API call), but unsupported parameters will  not raise an error.
Most common ones to be used are ``units``, ``lang`` and (if needed) ``APPID``. So it may be a good idea to pass them
in the form of a settings dictionary:

```Python
>>> settings = {"units": "metric", "lang": "DE"}
>>> data = owm.get_current("Kassel,DE", **settings)

# settings containing APIKEY
>>> settings = {"APPID": 1111111111, "units": "metric"}
```

## Data objects
The main data object is ``openweathermapy.utils.NestedDict``, which extends Python's builtin ``dict`` 
by methods giving a more flexible access to the items as shown above. If a list of weather data (objects) is returned
``openweathermapy.utils.NestedDictList`` or ``openweathermapy.core.DataBlock`` is used. The latter one just adds
an attribute ``meta`` to the ``NestedDictList`` containing the meta data of the responses:
```python
# get current weather data (data point)
>>> data = owm.get_current("Kassel,DE")
>>> type(data)
openweathermapy.utils.NestedDict

# get forecast data (data block)
>>> data = owm.get_forecast_daily("London,UK")
>>> type(data)
openweathermapy.core.DataBlock

>>>type(data.meta)
openweathermapy.utils.NestedDict
```

## Views
A **view** is just a list of keys to extract data from the responses. So, you can define views like **summary**,
**minimal** etc. depending on your needs. This keeps everything as flexible as possible:

```Python
>>> views = {
...    "summary": ["main.temp", "main.pressure", "main.humidity"]
... }

>>> data = owm.get_current("London,UK", units="metric")
>>> data(*views["summary"])
(18.56, 1011, 63)

# return complete keys
>>> data.get_dict(views["summary"])
{'main.temp': 18.56, 'main.humidity': 63, 'main.pressure': 1011}

# return only last key
>>> data.get_dict(views["summary"], split_keys=True)
{'pressure': 1011, 'temp': 18.56, 'humidity': 63} 
```   
You can also load views from files in **json** format for example by using ``openweathermapy.utils.load_config``.

## Fetch current weather data
The ``city`` argument can be given as **name**, **id**, or **geographic coordinates**.
If you want to stay as close as possible to the original API, you can also skip the
first argument and use the parameters ``q``, ``id``, ``lat`` and ``lon`` or ``zip`` instead,
for details see **OpenWeatherMap.org's** API documentation:

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

# alternative access
>>> data(*keys)
(11.06, 58, 6.2)

# get data for 'Kassel,DE', 'Malaga,ES', 'New York,US'
>>> city_ids = (2892518, 2514256, 5128581)
>>> data = owm.get_current_for_group(city_ids, units="metric", lang="DE")
>>> data_malaga = data[1]

# find city by name and return data for match(es)
>>> data = owm.find_city("Malaga")

# get data for 5 cities around geographic coordinates
>>> location = (51.32, 9.5)
>>> data = owm.find_cities_by_geo_coord(location, 5)

# get data from station
>>> data = owm.get_current_from_station(4926)

# get stations by geographic coordinates
>>> location = (51.32, 9.5)
>>> data = owm.find_stations_by_geo_coord(location)
```

## Fetch forecast data
The ``city`` argument can be given in the same way as shown in the examples above.  

```Python
# get 3h forecast data
>>> data = owm.get_forecast_hourly("Kassel,DE", lang="DE")

# get daily forecast data for 7 days
>>> data = owm.get_forecast_daily("Kassel,DE", 7, units="metric")

# show meta data
>>> data.meta
{u'city': {u'country': u'DE', u'population': 0, u'id': 2892518,
u'coord': {u'lat': 51.316669, u'lon': 9.5}, u'name': u'Kassel'},
u'message': 0.0185, u'cod': u'200', u'cnt': 7}

# get coordinates and id
>>> data.meta("city.coord", "city.id")
({u'lat': 51.316669, u'lon': 9.5}, 2892518)

# select columns
>>> selection = data.select(["dt", "temp.min", "temp.max"])
>>> for line in selection:
...    line 
...
(1437044400, 16.63, 24.99)
(1437130800, 18.21, 30.17)
(1437217200, 14.96, 26.35)
(1437303600, 15.82, 23.49)
(1437390000, 15.52, 23.95)
(1437476400, 18.77, 29.11)
(1437562800, 14.67, 27.11)

# convert column "dt" to datetime string
>>> from datetime import datetime as dt
>>> conv = {"dt": lambda ts: str(dt.utcfromtimestamp(ts))}

>>> selection = data.select(["dt", "temp.min", "temp.max"], converters=conv)
>>> for line in selection:
...    line 
...
('2015-07-16 11:00:00', 16.63, 24.99)
('2015-07-17 11:00:00', 18.21, 30.17)
('2015-07-18 11:00:00', 14.96, 26.35)
('2015-07-19 11:00:00', 15.82, 23.49)
('2015-07-20 11:00:00', 15.52, 23.95)
('2015-07-21 11:00:00', 18.77, 29.11)
('2015-07-22 11:00:00', 14.67, 27.11)
```

## Fetch historical data
For a complete list of parameters, which can be passed,
please refer to **OpenWeatherMap.org's** API documention. 

```Python
# get historical data by city name
>>> data = owm.get_history("Kassel,DE")

# define time period
>>> from datetime import datetime as dt
>>> date_s = dt(2015, 4, 1).timestamp()
>>> date_e = dt(2015, 4, 6).timestamp()

# get historical data for given time period by city id
>>> data = owm.get_history(2892518, start=date_s, end=date_e)

# give start date and number of hours to be retured
>>> data = owm.get_history("London,UK", start=date_s, cnt=48)

# get historical data from station
>>> data = owm.get_history_from_station(4926)
```

# Pandas support
**Since Openweathermapy version 0.7.0**

For forecast and historical data it is possible to get ``pandas.DataFrame`` objects from the responses:
```python
>>> data = owm.get_forecast_daily("London,UK")

# keys will be used as column names
>>> selection = data.select_pandas(["dt", "main.temp", "wind.speed"])
>>> selection.set_index("dt")

# it is also possible to pass an index column to the function
>>> dates = data.get("dt")
>>> selection = data.select_pandas(["main.temp", "wind.speed"], index=dates)

>>> selection.to_csv()
```
