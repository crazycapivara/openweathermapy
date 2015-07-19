# Getting started
# API
## Function
* Description/Definition
* Parameters
* Return (Type)
* Examples

## get_current
~~~Python
def get_current(city=None, **params)
~~~
Get current weather data for given ``city``.

**Arguments**
~~~
city (str, int or tuple):
   name, id or geographic coordinates (latitude, longitude)

**params:
   units, lang[, zip, q, ...], see OWM API
~~~

**Examples**
~~~Python
# get data by city name
>>> data = get_current("Kassel,DE", lang=DE)
~~~

## get_current_for_group
~~~Python
def get_current_for_group(city_ids, **params)
~~~
Get current weather data for multiple cities.

~~~Python	
   Args:
      city_ids (tuple): list of city ids,
      **params: units, lang

   Example:
      # get data for 'Malaga,ES', 'Kassel,DE', 'New York,US'
      >>> city_ids = (2892518, 2514256, 5128581)
      >>> data = get_current_for_group(city_ids, units="metric")
~~~
