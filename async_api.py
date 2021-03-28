import asyncio
import os

import aiohttp
from aiofile import async_open
import json
from datetime import datetime


async def first_api(session):
    api = 'http://www.7timer.info/bin/api.pl?lon=36.232845&lat=49.988358&product=civillight&output=json'
    r = await session.request(method='GET', url=api)
    # print(r.text)
    res = []
    data = await r.json(content_type=None)
    for i in data['dataseries']:
        temp = i['temp2m']
        res.append((temp['max'] + temp['min']) / 2)
    #print(res)
    return res


async def second_api(session):
    async with async_open('/home/kvantonio/hillel/async_api/keys.json', 'r', encoding='utf-8') as f:
        data_key = await f.read()
        data_key = json.loads(data_key)
    r = await session.request(method='GET',
        url='https://api.therainery.com/forecast',
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
    data = await r.json(content_type=None)
    hours_in_day = 24
    time = 0
    while time <= 128:
        if time == 120:
            hours_in_day = 8
        res.append(data['data'][time]['airTemperature'])
        time += hours_in_day
    return res


async def third_api(session):
    async with async_open('/home/kvantonio/hillel/async_api/keys.json', 'r', encoding='utf-8') as f:
        data_key = await f.read()
        data_key = json.loads(data_key)
    key = data_key['third']
    api = 'https://api.weatherbit.io/v2.0/forecast/daily?city=Kharkiv&key='+key
    res = []

    r = await session.request(method='GET', url=api)
    data = await r.json(content_type=None)
    for i in range(7):
        res.append(data['data'][i]['temp'])
    #print(res)
    return res


async def main():
    async with aiohttp.ClientSession() as session:
        p = await asyncio.gather(first_api(session), second_api(session), third_api(session))
        res = [round(sum(val)/len(p), 1)for val in zip(*p)]
        print(res)


if __name__ == '__main__':
    start = datetime.now()
    asyncio.run(main())
    print('Finished')

    print(datetime.now() - start)


