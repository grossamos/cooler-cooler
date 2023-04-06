from db import get_current_temp, retrieve_enable_inner, retrieve_temp_threshold
from meross import turn_device_on, turn_device_off
import os
import asyncio

async def ctrl_check():
    current_temp_inside = int(get_current_temp(0))
    current_temp_outside = int(get_current_temp(1))

    temp_threshold_inner = retrieve_temp_threshold(0)
    temp_threshold_outside = retrieve_temp_threshold(1)

    inner_enabled = retrieve_enable_inner()

    if current_temp_outside > temp_threshold_outside and current_temp_inside < temp_threshold_inner:
        await turn_device_off()
    else:
        await turn_device_on()

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ctrl_check())
    loop.stop()
