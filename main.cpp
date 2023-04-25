// Filipe Cavalcanti 2023
// #include "src/weather_service.hpp"
#include "src/client.hpp"
#include "src/wrapper.h"

int main() {
  // WeatherStation *ws = new WeatherStation(685);
  WeatherStation *ws = weather_station_create(685);
  Client *client_1 = new Client("Client 1", ws);
  Client *client_2 = new Client("Client 2", ws);
  ws->UpdateStation();
  delete client_1;
  delete client_2;
  return 0;
}
