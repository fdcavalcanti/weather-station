file (GLOB station_files
    *.cpp
    *.hpp
)

add_library(weather_station SHARED ${station_files})
