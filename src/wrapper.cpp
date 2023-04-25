#include "wrapper.h"

WeatherStation* WrapperWeatherStation(float station_altitude) {
  WeatherStation* station = new WeatherStation(station_altitude);
  return station;
}

void WrapperUpdateStation(WeatherStation* station) {
  station->UpdateStation();
}

Client* WrapperClient(const char* name, WeatherStation* station) {
  Client* client = new Client(name, station);
  return client;
}

void WrapperDeleteClient(Client* client) {
  delete client;
}
