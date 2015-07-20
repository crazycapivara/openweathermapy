# Getting started
# API
## Functions
### get_current
```Python
def get_current(city=None, **params)
```
#### Description (docstring)
```
Get current weather data for ``city``.
	
Args:
   city (str, int or tuple): name, id
      or geographic coordinates (latidude, longitude)
  **params: units, lang[, zip, ...]
```
#### Examples
```Python
# get data by city name and country code
>>> data = get_current("Kassel,DE")
	
# get data by city id and set language to german (de)
>>> data = get_current(2892518, lang="DE")
	
# get data by latitude and longitude and return temperatures in Celcius
>>> location = (51.32, 9.5)
>>> data = get_current(location, units="metric")
	
# optional: skip city argument and get data by zip code
>>> data = get_current(zip="34128,DE") 
```

---
