file (GLOB station_files
    *.cpp
    *.hpp
)

add_library(weather_station STATIC ${station_files})
