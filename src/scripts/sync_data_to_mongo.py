import json
import os

import pandas as pd

from pymongo import MongoClient
from pymongo import ASCENDING
from dotenv import load_dotenv

load_dotenv()

mongo_connection_string = os.getenv("MONGODB_CONN_STR", "mongodb://host.docker.internal:27017/sensors")
db = MongoClient(mongo_connection_string).get_database()

with open('./data/Sensors.json') as json_file:
    sensors = json.load(json_file)

with open('data/machines.json') as json_file:
    machines = json.load(json_file)

print("inserting sensors and machines to mongo")
db.sensors.insert_many(sensors)
db.machines.insert_many(machines)

print("getting machines events from file")
machines_events_df = pd.read_csv("data/Machine's events.csv", delimiter=';')

print("converting type of 'Date time' column to datetime")
machines_events_df['Date time'] = pd.to_datetime(machines_events_df['Date time'], format='%d/%m/%Y %H:%M')

print("renaming column names")
machines_events_df = machines_events_df.rename(columns={'Date time': 'date_time',
                                                        'Machine id': 'machine_id', 'Machine event': 'machine_event'})

print("converting the dataframe to list of dicts to insert into mongo")
machines_events_list_of_dicts = machines_events_df.to_dict('records')

print("Inserting machines events into mongo")
db.machines_events.insert_many(machines_events_list_of_dicts)

print("mapping sensor ids to their names for further using")
sensor_ids_to_names = dict()
for sensor in sensors:
    sensor_ids_to_names[sensor['sensor_name']] = sensor['sensor_id']

sensors_values_df = pd.read_csv("data/Sensors' values.csv", delimiter=';')

print("converting type of 'Date time' column to datetime")
sensors_values_df['Date time'] = pd.to_datetime(sensors_values_df['Date time'], format='%d/%m/%Y %H:%M')

print("converting the dataframe to a format suitable for mongodb docs")
sensors_values_list_of_dicts = sensors_values_df.to_dict('records')

"""
The data format to insert the database is:
{
    "sensor_id": "TEK10",
    "sensor_name": "Temperature EK10",
    "machine_id": "DEC1",
    "date_time": "2020-09-12 12:00:00",
    "sensor_value": "239.97"
}
"""


"""
we keep the last valid sensor value as we loop through sensors_values_list_of_dicts
because we might have some wrong sensor values we cannot convert to float.
"""
last_valid_values = dict()


docs = []
for idx, single_row in enumerate(sensors_values_list_of_dicts):
    for key, value in single_row.items():
        if key == 'Date time' or key == 'Machine id':
            continue

        doc = dict()
        doc['sensor_name'] = key
        doc['sensor_id'] = sensor_ids_to_names[key]
        doc['date_time'] = single_row['Date time']
        doc['machine_id'] = single_row['Machine id']

        try:
            doc['sensor_value'] = float(single_row[key].replace(',', '.'))
            last_valid_values[key] = doc['sensor_value']
        except:
            print(single_row)
            print("Value is outlier. Inserting ", last_valid_values[key], "instead of ", single_row[key])
            print("---------------------------------------------------- \n")
            _sensor_value = last_valid_values[key]
            doc['sensor_value'] = _sensor_value

        docs.append(doc)

print("Inserting sensor values to sensor_values mongo collection")
db.sensor_values.insert_many(docs)
print("Creating index for sensor_id and date_time fields")
db.sensor_values.create_index([("date_time", ASCENDING), ("sensor_id", ASCENDING)], background=True)
