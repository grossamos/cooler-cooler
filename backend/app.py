from aiohttp import web
from meross import turn_device_on, turn_device_off, get_consumption
from auth import auth_middleware
from db import get_current_temp, set_current_temp, get_temperature_history, add_temperature_to_history, get_last_temperature_from_history, save_temperature_threshold, retrieve_temp_threshold, save_enable_inner, retrieve_enable_inner
from datetime import datetime, timezone
from ctrlcheck import ctrl_check

async def base_route(request):
    response_payload = {"message": "hello world", "status": "healthy"}
    return web.json_response(response_payload)


async def device_control(request):
    incoming_payload = await request.json()

    if incoming_payload["is_on"]:
        await turn_device_on()
    else:
        await turn_device_off()

    return web.json_response(incoming_payload["is_on"])


async def device_status(request):
    dialy_consumption, current_consumption = await get_consumption()
    power_history = []
    for consump in dialy_consumption:
        power_history.append(consump["total_consumption_kwh"])
    response_payload = {"is_on": current_consumption.power > 0, "current_power": current_consumption.power, "daily_power": power_history}
    return web.json_response(response_payload)

async def set_temperature_inner(request):
    return await set_temperature(request, 0)

async def set_temperature_outer(request):
    return await set_temperature(request, 1)

async def set_temperature(request, loc):
    incoming_payload = await request.json()
    temperature = incoming_payload["temperature"]
    time = datetime.now(timezone.utc).timestamp()
    set_current_temp(temperature, loc)

    last_temp = get_last_temperature_from_history(loc)
    if last_temp["time"] < time - 5 * 60:
        add_temperature_to_history({"time":time, "temperature": temperature}, loc)
    return web.json_response(temperature)

async def get_temerature_data_inner(request):
    return await get_temerature_data(request, 0)

async def get_temerature_data_outer(request):
    return await get_temerature_data(request, 1)

async def get_temerature_data(request, loc):
    history = get_temperature_history(loc)
    current_temp = get_current_temp(loc).decode("utf-8") 

    response_payload = {
        "history": history,
        "current_temp": current_temp
    }
    return web.json_response(response_payload)

async def set_temperature_threshold_inner(request):
    return await set_temperature_threshold(request, 0)

async def set_temperature_threshold_outer(request):
    return await set_temperature_threshold(request, 1)

async def set_temperature_threshold(request, loc):
    incoming_payload = await request.json()
    temperature = incoming_payload["temperature"]

    save_temperature_threshold(temperature, loc)
    return web.json_response(temperature)

async def get_temerature_threshold_inner(request):
    return await get_temerature_threshold(request, 0)

async def get_temerature_threshold_outer(request):
    return await get_temerature_threshold(request, 1)

async def get_temerature_threshold(request, loc):
    temperature = retrieve_temp_threshold(loc)
    print(temperature)
    return web.json_response(temperature)

async def set_enable_inner(request):
    incoming_payload = await request.json()
    enable = incoming_payload["enable"]
    save_enable_inner(enable)
    return web.json_response(enable)

async def get_enable_inner(request):
    enable = retrieve_enable_inner()
    return web.json_response(enable)

async def run_maintenance(request):
    await ctrl_check()
    return web.json_response({"status": "up to date"})


app = web.Application(middlewares=[auth_middleware])
app.add_routes([
    web.get("/", base_route),
    web.post("/device", device_control),
    web.get("/device", device_status),
    web.post("/temperature/inner", set_temperature_inner),
    web.post("/temperature/outer", set_temperature_outer),
    web.get("/temperature/inner", get_temerature_data_inner),
    web.get("/temperature/outer", get_temerature_data_outer),
    web.get("/threshold/inner", get_temerature_threshold_inner),
    web.get("/threshold/outer", get_temerature_threshold_outer),
    web.post("/threshold/inner", set_temperature_threshold_inner),
    web.post("/threshold/outer", set_temperature_threshold_outer),
    web.get("/enable", get_enable_inner),
    web.post("/enable", set_enable_inner),
    web.post("/maintenance", run_maintenance)
])

if __name__ == "__main__":
    web.run_app(app)
