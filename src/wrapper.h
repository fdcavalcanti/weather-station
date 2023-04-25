#ifndef SRC_WRAPPER_H_
#define SRC_WRAPPER_H_

#ifdef __cplusplus
#include "weather_service.hpp"

extern "C" {
  WeatherStation* weather_station_create(float station_altitude) {
    WeatherStation* station = new WeatherStation(station_altitude);
    return station;
  }
}

#endif

#endif  // SRC_WRAPPER_H_
