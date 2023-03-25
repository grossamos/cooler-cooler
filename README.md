# IOT Cooler
## Development Setup
First setup the python venv for the backend:
```bash
cd backend
mkdir venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export REDIS_HOST=localhost
```

Next start a dev server for the frontend:
```bash
cd frontend
python3 -m http.server
```

Finally start redis via docker:
```bash 
docker run -d redis
```

## Motivation & Concept
The idea for this project is to optimise a cooling room in our house.
The cooling unit is plugged into a basic power socket, so this project will attempt to combine multiple data points (temperature in the room, temperature outside the room and power usage).
The cooler itself operates very inefficiently. 
It has two components that are controlled seperately; a cooling unit and a ventilation unit.
On hot days the ventilation unit often runs non-stop (because it is controlled by a sensor outside the room) and doesn't aid in cooling it down.

Potential power saving optimisations include:
- only cooling while its cold outside (ex. at night) ~ manual temperature threshold
- disabling cooling when power usage is too high ~ manual threshold 

Other features we need:
- Manual Override
- Authentification
- Histogram of when it was on and how much power was used & what the temperature was inside
