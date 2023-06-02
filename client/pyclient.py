import requests
import time

CLIENT_REG_URL = "http://192.168.1.89:8000/clients/2"

x = requests.post(CLIENT_REG_URL)
print(x.json())

while True:
    r = requests.get(CLIENT_REG_URL)
    print(r.json())
    time.sleep(10)

