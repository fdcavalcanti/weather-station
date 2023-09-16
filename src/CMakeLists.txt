set (CLIENT client.cpp client.hpp observer.hpp)
set (STATION station.cpp station.hpp common.hpp)
set (WRAPPER wrapper.cpp wrapper.h)
add_library(weather_station SHARED ${CLIENT} ${STATION} ${WRAPPER})
