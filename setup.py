from setuptools import setup

with file("README.md") as f:
	long_description = f.read()

setup(
	name="openweathermapy",
	version="0.6.0",
	url="https://github.com/crazycapivara/openweathermapy",
	author="Stefan Kuethe",
	author_email="crazycapivara@gmail.com",
	license="GPLv3",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intendend Audiance :: Users & Devolopers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3.2",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Topic :: Utilities" 
	],
	keywords="openweathermap, weather data, forecast data, free weather",
	description="Python package wrapping OpenWeatherMaps's API 2.5",
	long_description = long_description,
	packages = ["openweathermapy"]
)
