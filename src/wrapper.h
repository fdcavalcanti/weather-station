#ifndef SRC_WRAPPER_H_
#define SRC_WRAPPER_H_
#include <string.h>

#ifdef __cplusplus
#include "client.hpp"
#include "weather_service.hpp"
extern "C" {
#endif

WeatherStation* WrapperWeatherStation(float station_altitude);
void WrapperUpdateStation(WeatherStation* station);
Client* WrapperClient(char* name, WeatherStation* station);
void WrapperDeleteClient(Client* client);
void WrapperDisplayClient(Client* client, char* buffer);

#ifdef __cplusplus
}
#endif

#endif  // SRC_WRAPPER_H_
