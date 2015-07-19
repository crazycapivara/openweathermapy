# Getting started
# API
## Function
* Description/Definition
* Parameters
* Return (Type)
* Examples

## get_current
### Description
~~~Python
def get_current(city=None, **params)
~~~
Get current weather data for given **city**.
### Parameters
``city`` (str, int or tuple)

	name, id or geographic coordinates (latitude, longitude)

``**params``

	units, lang[, zip, q, ...]

### Examples
~~~Python
# get data by city name
>>> data = get_current("Kassel,DE", lang=DE)
~~~
