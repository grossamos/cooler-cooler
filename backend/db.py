import redis
import json
import os

REDIS_HOST = os.environ.get("REDIS_HOST")
redis_db = redis.Redis(host=REDIS_HOST, port=6379, db=0)

def loc_str(loc):
    if loc == 0:
        return "_inside"
    elif loc == 1:
        return "_outside"

def set_current_temp(temp, loc):
    redis_db.set("current_temp" + loc_str(loc), temp)


def get_current_temp(loc):
    temp = redis_db.get("current_temp" + loc_str(loc))
    if temp != None:
        return temp
    else:
        return 0


def add_temperature_to_history(temp, loc):
    temp_json = json.dumps(temp)
    redis_db.lpush("temp_history" + loc_str(loc), temp_json)
    redis_db.ltrim("temp_history" + loc_str(loc), 0, 3 * 24 * 12) # 3 days, every hour, every 5 min


def get_temperature_history(loc):
    history_length = redis_db.llen("temp_history" + loc_str(loc))
    history_raw = redis_db.lrange("temp_history" + loc_str(loc), 0, history_length) # 3 days, every hour, every 5 min
    history = unmarshal_temp_array(history_raw)

    for entry in history_raw:
        history.append(json.loads(entry))

    return history


def get_last_temperature_from_history(loc):
    history_raw = redis_db.lrange("temp_history" + loc_str(loc), 0, 1)
    history = unmarshal_temp_array(history_raw)
    if len(history) == 0:
        return {"temperature": 0, "time": 0}
    else:
        return history[0]


def unmarshal_temp_array(temps_raw):
    temps = []

    for entry in temps_raw:
        temps.append(json.loads(entry))

    return temps

def save_temperature_threshold(temp, loc):
    temp_json = json.dumps(temp)
    redis_db.set("temp_threshold" + loc_str(loc), temp_json)

def retrieve_temp_threshold(loc):
    temp = redis_db.get("temp_threshold" + loc_str(loc))
    if temp != None:
        return json.loads(temp)
    else:
        return 0

def save_enable_inner(enable):
    enable_json = json.dumps(enable)
    redis_db.set("enable_inner", enable_json)

def retrieve_enable_inner():
    enable_json = redis_db.get("enable_inner")
    return json.loads(enable_json)
