openweathermapy
===============

Python package wrapping *OpenWeatherMap.org’s* API 2.5.

As *OpenWeatherMap* returns data mostly in the form of nested
dictionaries, *openweathermapy* gives a simple API to access items in a
comfortable way:

.. code:: python

    # classic access
    item = data["main"]["temp"]

    # openweathermapy access
    item = data("main.temp")

    # access multiple items at once
    >>> items = data("main.temp", "wind.speed")

Status
======

Development (Alpha)

Version
=======

0.6.5

Installation
============

.. code:: bash

    ~$ python setup.py install

Documentation
=============

Besides the examples in this file, please use Python’s builtin help
functionality. Further documentation based on the docstrings is planned.

Usage
=====

.. code:: python

    >>> import openweathermapy.core as owm

All parameters defined in *OpenWeatherMap’s* API documentation can be
passed to the functions in *openweathermapy* as keyword arguments
``**params``. The query string always depends on the request (API call),
but unsupported parameters will (normally) not raise an error. Most
common ones to be used are ``units``, ``lang`` and (if needed)
``APPID``. So, it may be a good idea to pass them in the form of a
settings dictionary:

.. code:: python

    >>> settings = {"units": "metric", "lang": "DE"}
    >>> data = owm.get_current("Kassel,DE", **settings)

    # settings containing APIKEY
    >>> settings = {"APPID": 1111111111, "units": "metric"}

**Data objects and views**

The main data object is ``openweathermapy.utils.NestedDict``, which
extends Python’s builtin ``dict`` by methods giving a more flexible
access to the items as shown above. If a list of weather data (objects)
is returned ``openweathermapy.utils.NestedDictList`` or
``openweathermapy.core.DataBlock`` is used. The latter one just adds an
attribute ``meta`` to the ``NestedDictList`` containing the meta data of
the responses.

A **view** is just a list of keys to extract data from the responses.
So, you can define views like *summary*, *minimal* etc. depending on
your needs. This keeps everything as flexible as possible:

.. code:: python

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

You can also load views from files in *json* format for example by using
``openweathermapy.utils.load_config``.

**Current weather data**

**City** can be given as *name*, *id*, or *geographic coordinates*. If
you want to stay as close as possible to the original API, you can also
skip the first argument and use the parameters ``q``, ``id``, ``lat``
and ``lon`` or ``zip`` instead. For details see *OpenWeatherMap’s* API
documentation.

.. code:: python

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

    # get data for 'Malaga,ES', 'Kassel,DE', 'New York,US'
    >>> city_ids = (2892518, 2514256, 5128581)
    >>> data = owm.get_current_for_group(city_ids, units="metric", lang="DE")
    >>> data_malaga = data[0]

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

**Forecast data**

**City** can be given in the same way as shown in the examples above.

.. code:: python

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
    >>> data.meta(*["city.coord", "city.id"])
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

**Historical data**

For a complete list of parameters as ``start``, ``end`` etc., which can
be passed, please refer to *OpenWeatherMap’s* API documention.

.. code:: python

    # get historical data for city
    >>> data = owm.get_history("Kassel,DE")

    # get historical data from station
    >>> data = owm.get_history_from_station(4926)

**Customization**

You can customize or extend the lib to your needs by using the wrapper
function ``wrap_get`` or the decorator class ``GetDecorator``. Both are
more or less the same. As first argument the *appendix* to the *base
url* needs to be given. Optionally a *dictionary with parameters* and a
*data converter* can be passed.

.. code:: python

    # show base url
    >>> owm.BASE_URL
    'http://api.openweathermap.org/data/2.5/'

    # base url for fetching current weather data
    >>> appendix = "weather"
    >>> owm.BASE_URL+appendix
    'http://api.openweathermap.org/data/2.5/weather'

    # create a function to get current weather data and return temperatures in Celsius (units="metric") 
    >>> f = wrap_get("weather", dict(units="metric"))
    >>> data = f("London,UK")
    >>> data_de = f(zip="34128,DE", lang="DE")

