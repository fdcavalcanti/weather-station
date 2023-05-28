from pathlib import Path
import time
import datetime
import ctypes
import os

from database.database import add_reading_to_database, create_database

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
    buffer = ctypes.create_string_buffer(30)
    timestamp = datetime.datetime.now().strftime("%y%m%d-%H:%M:%S")
    STATION_LIB.WrapperDisplayClient(CLIENT, buffer)
    data = buffer.value.decode().split(",")
    temperature, pressure, humidity = data[0], data[1], 0
    print(f"{timestamp} -> Temperature: {temperature} | Pressure: {pressure} | Humidity: {humidity}")
    return timestamp, temperature, pressure, humidity


if __name__ == "__main__":
    # Register this script as a client
    print("Starting Weather Logging")
    while True:
        time.sleep(1)
        STATION_LIB.WrapperUpdateStation(WEATHER_STATION)
        data = read_station_data()
