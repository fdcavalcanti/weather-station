#ifndef SRC_WRAPPER_H_
#define SRC_WRAPPER_H_

#ifdef __cplusplus
#include "weather_service.hpp"
#include "client.hpp"
extern "C" {
#endif  

WeatherStation* WrapperWeatherStation(float station_altitude);
void WrapperUpdateStation(WeatherStation* station);
Client* WrapperClient(const char* name, WeatherStation* station);
void WrapperDeleteClient(Client* client);

#ifdef __cplusplus
}
#endif

#endif  // SRC_WRAPPER_H_
