import json, urllib.request
from fwi import *

ffmc = 0.0
dmc = 0.0
dc = 0.0
isi = 0.0
temp = 0.0
rh = 0.0
wind = 0.0
url = "http://api.openweathermap.org/data/2.5/weather?lat={}&" \
      "lon={}&appid=997248ab2a9c56c05cf48c93efca9b27".format(41.9, -7)

j = json.load(urllib.request.urlopen(url))
print(j)
temp = j['main']['temp'] - 273.15
wind = j['wind']['speed'] * 3.6
rh = j['main']['humidity']
rain = ((j['rain']['3h']) / 6) / ((742300000 / 9) ** 2)
ffmc = FFMC(temp, rh, wind, j['rain']['3h'] * 8, 57.45)
dmc = DMC(temp,rh,rain,146.2,)
