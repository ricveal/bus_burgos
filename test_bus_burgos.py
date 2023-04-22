import asyncio

import aiohttp

import bus_burgos


def test_fetching_all_bus_stops():
    async def test():
        async with aiohttp.ClientSession() as client:
            result = await bus_burgos.get_all_bus_stops(client)
            assert len(result) == 490
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())


def test_all_info_from_bus_stops():
    async def test():
        async with aiohttp.ClientSession() as client:
            result = await bus_burgos.get_all_bus_stops(client)
            bus_stop = next(x for x in result if x.name == "San Pablo Progreso")
            assert bus_stop.latitude == 42.337335244527175
            assert bus_stop.longitude == -3.699231875463945
            assert bus_stop.id == "200"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())


def test_fetching_info_from_one_bus_stop():
    async def test():
        async with aiohttp.ClientSession() as client:
            result = await bus_burgos.get_bus_stop(client, "200")
            assert len(result.get_times_by_line("02")) > 0
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())


def test_fetching_next_bus(mocker):
    async def test():
        async with aiohttp.ClientSession() as client:
            result = await bus_burgos.get_bus_stop(client, "200")
            assert result.get_next_bus("02").destination == "Estacion Tren"
            assert result.get_next_bus("02").seconds == 1200
    loop = asyncio.get_event_loop()
    mockValue = [
        bus_burgos.Estimation.from_json({
            "destination": "Plaza Vega - Catedral",
            "seconds": 3320,
            "meters": 0,
            "vehicle": 0
        }),
        bus_burgos.Estimation.from_json({
            "destination": "Estacion Tren",
            "seconds": 1200,
            "meters": 0,
            "vehicle": 0
        }),
        bus_burgos.Estimation.from_json({
            "destination": "Plaza España",
            "seconds": 2000,
            "meters": 0,
            "vehicle": 0
        }),
    ]
    mocker.patch("bus_burgos.BusStopWithEstimations.get_times_by_line", return_value=mockValue)
    loop.run_until_complete(test())
