import json
import os
from datetime import datetime

import requests


def first_api():
    api = 'http://www.7timer.info/bin/api.pl?lon=36.232845&lat=49.988358&product=civillight&output=json'
    r = requests.get(api)
    res = []
    data = r.json()
    for i in data['dataseries']:
        temp = i['temp2m']
        res.append((temp['max'] + temp['min']) / 2)
    return res


def second_api(key):
    r = requests.get(
        'https://api.therainery.com/forecast',
        params={
            'latitude': 49.988358,
            'longitude': 36.232845,
            'model': 'GFS_13',
        },
        headers={
            'x-api-key': key
        }
    )
    res = []
    data = r.json()
    t = 24
    j = 0
    while j <= 128:
        if j == 120:
            t = 8
        res.append(data['data'][j]['airTemperature'])
        j += t
    return res


def third_api(key):
    api = 'https://api.weatherbit.io/v2.0/forecast/daily?city=Kharkiv&key=' + key
    res = []
    r = requests.get(api)
    data = r.json()
    for i in range(7):
        res.append(data['data'][i]['temp'])
    return res


def fourth_api():
    api = 'https://api.met.no/weatherapi/locationforecast/2.0/compact.json?lat=49.988358&lon=36.232845'
    headers = {
        'User-Agent': 'Mozilla/5.0(X11;Ubuntu;Linuxx86_64;rv: 87.0)Gecko/20100101Firefox/87.0'
    }
    r = requests.get(api, headers=headers)
    data = r.json()
    t = 24
    j = 0
    res = []
    while j <= 84:
        if j >= 60:
            t = 4
        res.append(data['properties']['timeseries'][j]['data']['instant']['details']['air_temperature'])
        j += t
    return res


if __name__ == '__main__':
    start = datetime.now()
    with open(os.path.dirname(os.path.abspath(__file__)) +'/keys.json', 'r') as f:
        data_key = json.loads(f.read())

    p = (first_api(),
         # second_api(data_key['second']),
         third_api(data_key['third']),
         fourth_api())
    res = [round(sum(val) / len(p), 1) for val in zip(*p)]
    print(res)
    print(datetime.now() - start)
