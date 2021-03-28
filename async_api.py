import asyncio
import aiohttp
from datetime import datetime
import keys


async def first_api(session):
    api = 'http://www.7timer.info/bin/api.pl?lon=36.232845&lat=49.988358&product=civillight&output=json'
    r = await session.request(method='GET', url=api)
    res = []
    data = await r.json(content_type=None)
    for i in data['dataseries']:
        temp = i['temp2m']
        res.append((temp['max'] + temp['min']) / 2)

    return res


async def second_api(session):
    r = await session. \
        request(method='GET',
                url='https://api.therainery.com/forecast',
                params={
                    'latitude': 49.988358,
                    'longitude': 36.232845,
                    'model': 'GFS_13',
                },
                headers={'x-api-key': keys.SECOND}
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
    api = 'https://api.weatherbit.io/v2.0/forecast/daily?city=Kharkiv&key=' + keys.THIRD
    res = []
    r = await session.request(method='GET', url=api)
    data = await r.json(content_type=None)
    for i in range(7):
        res.append(data['data'][i]['temp'])
    return res


async def fourth_api(session):
    api = 'https://api.met.no/weatherapi/locationforecast/2.0/compact.json?lat=49.988358&lon=36.232845'
    headers = {
        'User-Agent': 'Mozilla/5.0(X11;Ubuntu;Linuxx86_64;rv:87.0)Gecko/20100101Firefox/87.0'
    }
    r = await session.request(method='GET', url=api, headers=headers)
    data = await r.json(content_type=None)
    hours_in_day = 24
    time = 0
    res = []
    while time <= 84:
        if time >= 60:
            hours_in_day = 4
        res.append(data['properties']['timeseries'][time]['data']['instant']['details']['air_temperature'])
        time += hours_in_day
    return res


async def main():
    async with aiohttp.ClientSession() as session:
        p = await asyncio.gather(
            first_api(session),
            second_api(session),
            third_api(session),
            fourth_api(session)
        )
        res = [round(sum(val) / len(p), 1) for val in zip(*p)]
        print(res)


if __name__ == '__main__':
    start = datetime.now()
    asyncio.run(main())
    print('Finished')
    print(datetime.now() - start)
