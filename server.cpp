#include <iostream>
#include <chrono>
#include <unistd.h>
#include "weather_service.hpp"

#define CAMPINAS_ALTITUDE 685
#define SAMPLE_INTERVAL 60

int main() {
  std::cout << "Weather Station bring up" << std::endl;
  WeatherStation *ws = new WeatherStation(CAMPINAS_ALTITUDE);

  while(1) {
    std::cout << "Updating Station" << std::endl;
    ws->UpdateStation();
    auto start = std::chrono::steady_clock::now();
    float diff = 0;
    while (diff < SAMPLE_INTERVAL) {
      auto end = std::chrono::steady_clock::now();
      diff = std::chrono::duration_cast<std::chrono::seconds>(end-start).count();
      usleep(1000000);
    }
  }
}
