default = [
	"name",
	"main.temp",
	"main.humidity",
	"wind.speed"		
]

minimal = [
	"main.temp",
	"main.humidity",
	"wind.speed"		
]

test = ["name"]+minimal

current = {
	"default": default,
	"minimal": minimal
}

info = {
	"main.temp": {
		"unit": "Celsius"
	},
	"main.humidity": {
		"unit": "%"
	}
}
