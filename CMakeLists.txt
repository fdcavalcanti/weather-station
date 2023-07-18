cmake_minimum_required(VERSION 3.10)
project (WeatherStation C CXX)

set (CMAKE_CXX_FLAGS  "-Wall -std=c++17 -O0 -fpic -fno-unwind-tables -Wnon-virtual-dtor -fno-rtti")
add_subdirectory(src)
file (GLOB main
    ${PROJECT_SOURCE_DIR}/main.cpp
)
file (GLOB server
      ${PROJECT_SOURCE_DIR}/server.cpp
)

include_directories (PUBLIC src/)
add_executable (main ${main})
add_executable (server ${server})
add_dependencies(main weather_station)
add_dependencies(server weather_station)
target_link_libraries(main ${PROJECT_SOURCE_DIR}/build/src/libweather_station.so)
target_link_libraries(server ${PROJECT_SOURCE_DIR}/build/src/libweather_station.so)
