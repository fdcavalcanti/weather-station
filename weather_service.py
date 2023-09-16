from pathlib import Path
import time
import datetime
import ctypes
import os

from database.database import add_reading_to_database, create_database, Measurement

SAMPLE_INTERVAL_S = 900
LOCAL_ALTITUDE = 685
DB_PATH = Path.home() / "weather-station" / "database" / "station.db"
STATION_SO_PATH = Path.home() / "weather-station" / "build" / "src" / "libweather_station.so"

# Get the .so file for the weather station
STATION_LIB = ctypes.CDLL(STATION_SO_PATH, mode=ctypes.RTLD_GLOBAL)
STATION_LIB.WrapperDisplayClient.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

# Initiate the weather station
WEATHER_STATION = STATION_LIB.WrapperWeatherStation(ctypes.c_float(LOCAL_ALTITUDE))
STATION_LIB.WrapperUpdateStation(WEATHER_STATION)

# Register the Raspberry client
CLIENT = STATION_LIB.WrapperClient("Rasp", WEATHER_STATION)


def read_station_data():
    cbuffer = ctypes.create_string_buffer(50)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    STATION_LIB.WrapperDisplayClient(CLIENT, cbuffer)
    data = cbuffer.value.decode().split(",")
    print(data)
    meas = Measurement(timestamp, float(data[0]), float(data[1]), float(data[2]), float(data[3]))
    return meas


if __name__ == "__main__":
    # Register this script as a client
    print("Starting Weather Logging")
    print(f"DB: {DB_PATH}")

    while True:
        STATION_LIB.WrapperUpdateStation(WEATHER_STATION)
        meas = read_station_data()
        add_reading_to_database(DB_PATH, meas)
        time.sleep(SAMPLE_INTERVAL_S)
