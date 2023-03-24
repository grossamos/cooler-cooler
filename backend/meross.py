import asyncio
import os

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = os.environ.get('MEROSS_EMAIL')
PASSWORD = os.environ.get('MEROSS_PASSWORD')

async def init_device():
    # login
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()
    await manager.async_device_discovery()

    # initialize device
    meross_devices = manager.find_devices(device_type="mss310")
    if len(meross_devices) < 1:
        raise Exception("no plugs found")

    plug = meross_devices[0]
    await plug.async_update()
    return http_api_client, manager, plug


async def close_device(manager, http_api_client):
    manager.close()
    await http_api_client.async_logout()

async def turn_device_on():
    http_api_client, manager, plug = await init_device()
    await plug.async_turn_on(channel=0)
    await close_device(manager, http_api_client)

async def turn_device_off():
    http_api_client, manager, plug = await init_device()
    await plug.async_turn_off(channel=0)
    await close_device(manager, http_api_client)

async def get_consumption():
    http_api_client, manager, plug = await init_device()
    daily_consumption = await plug.async_get_daily_power_consumption()
    current_consumption = await plug.async_get_instant_metrics()
    await close_device(manager, http_api_client)
    return daily_consumption, current_consumption
