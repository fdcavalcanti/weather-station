import requests

ADDRESS = "http://192.168.1.89:8000/"

if __name__ == "__main__":
    req = requests.get(ADDRESS)
    print(req)
    # Register a new observer number 5
    req = requests.post(ADDRESS + "clients/2")
    print(req.json())
    # Update the station readings
    req = requests.get(ADDRESS + "station")
    # Read the temperature on this client
    req = requests.get(ADDRESS + "clients/2")
    print(req)
