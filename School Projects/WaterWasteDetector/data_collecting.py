"""Indsamler temperatur data fra enhed

    Returns:
        Log som gemmes som en CSV fil, denne indholder temperatur målingerne
    """
import csv
import os
from datetime import date, datetime

from w1thermsensor import Sensor, W1ThermSensor

HEADERS = ["Time", "Room Temp", "Pipe Temp", "Diff"]
TODAYS_DATE = date.today().strftime("%d-%m-%y")
TIME_NOW = datetime.now().strftime("%d-%m-%y %H:%M:%S")
FILENAME = f"logs/log_data_{TODAYS_DATE}.csv"

sensor_keys = [sensor.id for sensor in W1ThermSensor.get_available_sensors()]
sensor_pipe = W1ThermSensor(
    sensor_type=Sensor.DS18B20, sensor_id=sensor_keys[0])
sensor_pipe.set_resolution(12)
sensor_room = W1ThermSensor(
    sensor_type=Sensor.DS18B20, sensor_id=sensor_keys[1])
sensor_room.set_resolution(12)


def csv_writer(file):
    return csv.DictWriter(file, [HEADERS[0], HEADERS[1], HEADERS[2], HEADERS[3]], lineterminator="\n")



if not os.path.exists(FILENAME):
    with open(FILENAME, "w") as f:
        file = csv_writer(f)
        file.writeheader()


with open(FILENAME, "a") as f:
    file = csv_writer(f)
    temp_pipe = sensor_pipe.get_temperature()
    temp_room = sensor_room.get_temperature()
    diff = temp_pipe - temp_room
    data_dict = {HEADERS[0]: TIME_NOW,
                 HEADERS[1]: temp_pipe,
                 HEADERS[2]: temp_room,
                 HEADERS[3]: diff}
    file.writerow(data_dict)
