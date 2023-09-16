// Filipe Cavalcanti 2023
#ifndef SRC_WEATHER_SERVICE_HPP_
#define SRC_WEATHER_SERVICE_HPP_
#include <iostream>
#include <cstdint>
#include <cmath>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <filesystem>

#include <unistd.h>
#include "common.hpp"
#include "observer.hpp"
#include "subject.hpp"

class WeatherStation : public Subject {
 public:
  explicit WeatherStation(float station_altitude);
  ~WeatherStation() = default;
  void RegisterObserver(Observer *observer) override;
  void RemoveObserver(Observer *observer) override;
  void NotifyObservers() override;
  void UpdateStation();
  float GetTemperature(Sensor sensor);
  float GetPressure();
  float GetHumidity();
 private:
  const std::filesystem::path iio_path_ = "/sys/bus/iio/devices/";
  #ifdef BMP280_DEVICE_0
  std::string bmp280_device = "iio:device0";
  std::string dht22_device = "iio:device1";
  #else
  std::string bmp280_device = "iio:device1";
  std::string dht22_device = "iio:device0";
  #endif
  const std::filesystem::path iio_temperature_bmp280_ = iio_path_ / bmp280_device / "in_temp_input";
  const std::filesystem::path iio_temperature_dht22_ = iio_path_ / dht22_device / "in_temp_input";
  const std::filesystem::path iio_pressure_ = iio_path_ / bmp280_device / "in_pressure_input";
  const std::filesystem::path iio_humidity_ = iio_path_ / dht22_device / "in_humidityrelative_input";
  std::vector<Observer*> observers_;
  float station_altitude_;
  WeatherStationData current_weather_data_;
  float ConvertToRelativePressure(float pressure, float altitude,
                                  float temperature);
  std::string ReadLineFromFile(const char *filename);
};

#endif  // SRC_WEATHER_SERVICE_HPP_
