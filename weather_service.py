from pathlib import Path
import time
import datetime
import ctypes
import os

from database.database import add_reading_to_database, create_database, Measurement

SAMPLE_INTEVAL_S = 900
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
    cbuffer = ctypes.create_string_buffer(30)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    STATION_LIB.WrapperDisplayClient(CLIENT, cbuffer)
    data = cbuffer.value.decode().split(",")
    meas = Measurement(timestamp, float(data[0]), float(data[1]), float(0))
    print(f"{meas.timestamp} -> Temperature: {meas.temperature} | Pressure: {meas.pressure} | Humidity: {meas.humidity}")
    return meas


if __name__ == "__main__":
    # Register this script as a client
    print("Starting Weather Logging")
    print(f"DB: {DB_PATH}")

    while True:
        time.sleep(SAMPLE_INTERVAL_S)
        STATION_LIB.WrapperUpdateStation(WEATHER_STATION)
        meas = read_station_data()
        add_reading_to_database(DB_PATH, meas)

