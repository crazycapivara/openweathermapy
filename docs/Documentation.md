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
### Arguments
* ``city`` (str, int or tuple): name, id or geographic coordinates (latitude, longitude)
* ``**params``: units, lang[, zip, q, ...], see OWM API

### Examples
~~~Python
# get data by city name
>>> data = get_current("Kassel,DE", lang=DE)
~~~
