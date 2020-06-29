"""
Connect to a Hive home thermostat and save the temperature to a file.
Requires env variable HiveU and HiveP with your Hive username and password respectively
"""
import os
import time
from datetime import datetime

import requests

import db_utils

# TODO get rid once file based storage is removed
TEMPERATURE_DATA_FILE = "temperature_data.txt"
GLOBAL_HEADERS = {"Content-Type": "application/vnd.alertme.zoo-6.5+json",
                  "Accept": "application/vnd.alertme.zoo-6.5+json",
                  "X-Omnia-Client": "Hive Web Dashboard", }


def authenticate(username: str, password: str) -> str:
    """Authenticate with the Hive and return the session id used in further communications"""
    data = {"sessions": [{
        "username": username,
        "password": password,
        "caller": "WEB",
    }]}
    r = requests.post("https://api-prod.bgchprod.info:443/omnia/auth/sessions", json=data, headers=GLOBAL_HEADERS)
    if r.status_code != 200:
        return ''
    dictionary = r.json()
    session_id_ = dictionary["sessions"][0]["sessionId"]
    return session_id_


def get_temperature(session_id_: str) -> float:
    """Request the temperature. Session id is required in the header """
    headers = GLOBAL_HEADERS.copy()
    headers["X-Omnia-Access-Token"] = session_id_
    response = requests.get("https://api-prod.bgchprod.info:443/omnia/nodes", headers=headers)
    return get_temperature_from_response(response)


def get_temperature_from_response(response):
    """Parse the response json for the temperature reading of the hive"""
    if response.status_code == 200:
        dictionary = response.json()
        current_temperature = dictionary["nodes"][3]["features"]["temperature_sensor_v1"]["temperature"][
            "reportedValue"]
        return current_temperature
    return None


def run(period=600):
    """Get the temperature from the hive"""
    while 1:
        session_id = authenticate(os.getenv("HiveU"), os.getenv("HiveP"))
        if session_id:
            temperature = get_temperature(session_id)
            if temperature:
                date_time = datetime.now().isoformat()
                export_string = "{0}\t{1}\n".format(date_time, str(temperature))
                print(export_string)
                # TODO Get rid of writing to a file
                with open(TEMPERATURE_DATA_FILE, "a") as temp_file:
                    temp_file.write(export_string)
                db_utils.store_measurement(date_time, str(temperature))
        time.sleep(period)


# Temp. Run the script
run()
