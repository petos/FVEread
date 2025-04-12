import json
import re
import requests

# Configuration
OPTCFGFILE = "/opt/cfg/lowtarif.cfg"
JSONOUTPUT = True
VERBOSE = False

ISLOWTARIF = False
LOWTARIFSENSOR = "sensor.low_tarif"
LOWTARIFSTATE = "on"
OUTSIDESENSOR = "sensor.outside_temperature"
TEMP = None

STARTSTOPDEVICES = {}

# Utility functions
def errorPrint(msg):
    print(f"ERROR: {msg}")

def verbPrint(msg):
    if VERBOSE:
        print(f"VERBOSE: {msg}")

def parseHAAPI(entity_id: str, attribute: str = "state") -> str:
    try:
        url = f"http://homeassistant.petos.eu:8123/api/states/{entity_id}"
        headers = {"Authorization": "Bearer YOUR_LONG_LIVED_ACCESS_TOKEN"}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data[attribute] if attribute in data else data.get("state")
        else:
            errorPrint(f"Failed to get {entity_id}: {resp.status_code}")
    except Exception as e:
        errorPrint(f"Exception during API fetch for {entity_id}: {e}")
    return ""

def getTempViaHAAPI():
    global TEMP
    val = parseHAAPI(OUTSIDESENSOR)
    try:
        TEMP = float(val)
    except ValueError:
        errorPrint(f"Cannot convert temperature '{val}' to float")

def getLowViaHAAPI():
    global ISLOWTARIF
    val = parseHAAPI(LOWTARIFSENSOR)
    if val == LOWTARIFSTATE:
        ISLOWTARIF = True
    else:
        ISLOWTARIF = False

# Device parsing and management
def parseThermalDevice(line: str):
    parts = re.split(r'\s+', line.strip())
    if len(parts) < 5:
        errorPrint(f"Skipping invalid config line: {line}")
        return

    dev_id, sensor, tempmin, tempmax, name = parts[:5]
    try:
        STARTSTOPDEVICES[dev_id] = {
            "name": name,
            "entity": dev_id,
            "sensor": sensor,
            "tempmin": float(tempmin),
            "tempmax": float(tempmax),
        }
    except ValueError:
        errorPrint(f"Invalid temp values in config line: {line}")

def decideOnOff(device, temp):
    actions = []
    name = device['name']
    dev = device['entity']
    tempmin = device['tempmin']
    tempmax = device['tempmax']

    if temp < tempmin:
        actions.append(dev)
        verbPrint(f"{name} ON (temp {temp} < {tempmin})")
    elif temp > tempmax:
        actions.append(f"!{dev}")
        verbPrint(f"{name} OFF (temp {temp} > {tempmax})")
    else:
        verbPrint(f"{name} no action (temp {temp})")

    return actions

def manageThermalDevicesLowTarif():
    result = []
    for idx, device in STARTSTOPDEVICES.items():
        sensor = device['sensor']
        val = parseHAAPI(sensor)
        if not val:
            errorPrint(f"[{idx}] {device['name']}: No value for sensor {sensor}")
            continue

        try:
            temperature = float(val)
        except ValueError:
            errorPrint(f"[{idx}] {device['name']}: Cannot convert '{val}' to float")
            continue

        actions = decideOnOff(device, temperature)
        result.extend(actions)
    return result

def updateJSONforDevices(actions):
    out = []
    for entity in actions:
        if entity.startswith("!"):
            out.append({"entity_id": entity[1:], "service": "turn_off"})
        else:
            out.append({"entity_id": entity, "service": "turn_on"})
    return out

def mainLoop():
    getTempViaHAAPI()
    getLowViaHAAPI()

    actions = []
    if ISLOWTARIF:
        actions = manageThermalDevicesLowTarif()
    else:
        verbPrint("Not low tarif – skipping thermal management.")

    result = updateJSONforDevices(actions)
    if JSONOUTPUT:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    try:
        with open(OPTCFGFILE, "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    parseThermalDevice(line)
    except FileNotFoundError:
        errorPrint(f"Config file not found: {OPTCFGFILE}")

    mainLoop()
