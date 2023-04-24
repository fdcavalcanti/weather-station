cmake_minimum_required(VERSION 3.10)
project (WeatherStation CXX)

set (CMAKE_CXX_FLAGS  "-Wall -fno-unwind-tables -Wnon-virtual-dtor -fno-rtti")

file (GLOB station_files
    ${PROJECT_SOURCE_DIR}/src/*.cpp
    ${PROJECT_SOURCE_DIR}/src/*.hpp
)

file (GLOB main
    ${PROJECT_SOURCE_DIR}/main.cpp
)

include_directories (PUBLIC src/)
add_library(weather_station STATIC ${station_files})
add_executable (main ${main})
target_link_libraries(main ${PROJECT_SOURCE_DIR}/build/libweather_station.a)
