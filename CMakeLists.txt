cmake_minimum_required(VERSION 3.10)
project (WeatherStation C CXX)

set (CMAKE_CXX_FLAGS  "-Wall -std=c++17 -O0 -fpic -fno-unwind-tables -Wnon-virtual-dtor -fno-rtti")
add_subdirectory(src)

add_executable (main src/main.cpp)
target_link_libraries(main weather_station)
