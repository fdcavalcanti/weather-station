import ctypes
import os
from fastapi import FastAPI
from typing import Union

libpath = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "build", "src", "libweather_station.so"))
station_lib = ctypes.CDLL(libpath, mode=ctypes.RTLD_GLOBAL)
station = station_lib.weather_station_create
print(station_lib)

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return{"Hello": "World"}

# @app.get("/")
# def get_temperature():
#     temp = station_lib.GetTemperature()
#     return{"Temperature": temp}
