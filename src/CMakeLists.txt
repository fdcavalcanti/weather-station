file (GLOB station_files
    *.cpp
    *.hpp
    wrapper.h
)

add_library(weather_station SHARED ${station_files})
