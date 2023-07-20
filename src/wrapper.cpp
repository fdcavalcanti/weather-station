#include "wrapper.h"

WeatherStation* WrapperWeatherStation(float station_altitude) {
  WeatherStation* station = new WeatherStation(station_altitude);
  return station;
}

void WrapperUpdateStation(WeatherStation* station) {
  station->UpdateStation();
}

Client* WrapperClient(char* name, WeatherStation* station) {
  Client* client = new Client(name, station);
  return client;
}

void WrapperDeleteClient(Client* client) {
  delete client;
}

void WrapperDisplayClient(Client* client, char* buffer) {
  std::string data = client->Display();
  strncpy(buffer, data.c_str(), 50);
}
