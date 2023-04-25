cmake_minimum_required(VERSION 3.10)
project (WeatherStation CXX)

set (CMAKE_CXX_FLAGS  "-Wall -fno-unwind-tables -Wnon-virtual-dtor -fno-rtti")
add_subdirectory(src)
file (GLOB main
    ${PROJECT_SOURCE_DIR}/main.cpp
)

include_directories (PUBLIC src/)
add_executable (main ${main})
add_dependencies(main weather_station)
target_link_libraries(main ${PROJECT_SOURCE_DIR}/build/src/libweather_station.a)
