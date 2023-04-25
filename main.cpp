// Filipe Cavalcanti 2023
// #include "src/weather_service.hpp"
#include "src/wrapper.h"

int main() {
  // WeatherStation *ws = new WeatherStation(685);
  WeatherStation *ws = WrapperWeatherStation(685);
  Client *client_1 = WrapperClient("Client 1", ws);
  Client *client_2 = WrapperClient("Client 2", ws);
  WrapperUpdateStation(ws);
  WrapperDeleteClient(client_1);
  WrapperDeleteClient(client_2);
  return 0;
}
