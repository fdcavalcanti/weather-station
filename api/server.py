import ctypes
import asyncio
import os
import time
from fastapi import FastAPI
from fastapi.exceptions import HTTPException

libpath = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), "..", "build", "src", "libweather_station.so"
    )
)
station_lib = ctypes.CDLL(libpath, mode=ctypes.RTLD_GLOBAL)
station = station_lib.WrapperWeatherStation(ctypes.c_float(685))
station_lib.WrapperUpdateStation(station)
clients = {}

app = FastAPI()

async def station_update():
    while True:
        await asyncio.sleep(900)
        station_lib.WrapperUpdateStation(station)

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(station_update())


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/station")
def update_station():
    station_lib.WrapperUpdateStation(station)
    return {"Message": "done"}

@app.post("/clients/{client}")
def register_client(client: int):
    if client in clients:
        raise HTTPException(400, detail="Client already exists")
    station_lib.WrapperClient.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    print(f"Registering client: {client}")
    client_name = f"Client_{client}"
    cl = station_lib.WrapperClient(client_name.encode(), station)
    clients[client] = cl
    return {"Message": "done"}


@app.get("/clients/{client}")
def display_client_temperature(client: int):
    station_lib.WrapperDisplayClient.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    buffer = ctypes.create_string_buffer(30)
    if client > len(clients):
        raise HTTPException(status_code=404, detail="Client not initialized")
    station_lib.WrapperDisplayClient(clients[client], buffer)
    data = buffer.value.decode()
    temperature, pressure = data.split(",")[0], data.split(",")[1]
    return {"client": client, "temperature C": temperature, "pressure hPa": pressure}

