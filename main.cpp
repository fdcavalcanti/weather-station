// Filipe Cavalcanti 2023
// #include "src/weather_service.hpp"
#include <iostream>
#include "src/wrapper.h"

int main() {
  // WeatherStation *ws = new WeatherStation(685);
  char buffer[30];
  WeatherStation *ws = WrapperWeatherStation(685);
  Client *client_1 = WrapperClient("Client 1", ws);
  Client *client_2 = WrapperClient("Client 2", ws);
  WrapperUpdateStation(ws);
  WrapperDisplayClient(client_1, buffer);
  std::cout << buffer << std::endl;
  WrapperDeleteClient(client_1);
  WrapperDeleteClient(client_2);
  return 0;
}
