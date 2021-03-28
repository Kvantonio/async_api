import asyncio
import json

import requests
from datetime import datetime


def first_api():
    api = 'http://www.7timer.info/bin/api.pl?lon=36.232845&lat=49.988358&product=civillight&output=json'
    r = requests.get(api)
    # print(r.text)
    res = []
    data = r.json()
    for i in data['dataseries']:
        temp = i['temp2m']
        res.append((temp['max'] + temp['min']) / 2)

    return res


def second_api():
    with open('/home/kvantonio/hillel/async_api/keys.json', 'r') as f:
        data_key = json.loads(f.read())

    r = requests.get(
        'https://api.therainery.com/forecast',
        params={
            'latitude': 49.988358,
            'longitude': 36.232845,
            'model': 'GFS_13',
        },
        headers={
            'x-api-key': data_key['second']
        }
    )
    res = []
    data = r.json()
    #print(data)
    t = 24
    j = 0
    while (j <= 128):
        if j == 120:
            t = 8
        res.append(data['data'][j]['airTemperature'])
        # print(datetime.fromtimestamp(data[j]['timestamp']))
        j += t
    return res


def third_api():
    with open('/home/kvantonio/hillel/async_api/keys.json', 'r') as f:
        data = json.loads(f.read())
        key = data['third']
    api = 'https://api.weatherbit.io/v2.0/forecast/daily?city=Kharkiv&key=' + key
    res = []
    r = requests.get(api)
    data = r.json()
    for i in range(7):
        res.append(data['data'][i]['temp'])
    return res


if __name__ == '__main__':
    start = datetime.now()
    p = (first_api(), second_api(), third_api())
    res = [round(sum(val) / len(p), 1) for val in zip(*p)]
    print(res)
    print('Finished')

    print(datetime.now() - start)
