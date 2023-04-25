import ctypes
import os
from fastapi import FastAPI

libpath = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), "..", "build", "src", "libweather_station.so"
    )
)
station_lib = ctypes.CDLL(libpath, mode=ctypes.RTLD_GLOBAL)
station = station_lib.WrapperWeatherStation(ctypes.c_float(685))
station_lib.WrapperUpdateStation(station)
client_list = []

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.put("/clients/{client}")
def register_client(client: int):
    station_lib.WrapperClient.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    client_name = f"Client_{client}"
    cl = station_lib.WrapperClient(client_name.encode(), station)
    client_list.append(cl)
    return {"Message": "done"}


@app.get("/station")
def update_station():
    station_lib.WrapperUpdateStation(station)
    return {"Message": "done"}


@app.get("/clients/{client}")
def display(client: int):
    station_lib.WrapperDisplayClient.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    buffer = ctypes.create_string_buffer(30)
    if client > len(client_list):
        return {"Error": "Client not initialized"}
    station_lib.WrapperDisplayClient(client_list[client - 1], buffer)
    data = buffer.value.decode()
    temperature, pressure = data.split(",")[0], data.split(",")[1]
    return {"client": client, "temperature": temperature, "pressure": pressure}
