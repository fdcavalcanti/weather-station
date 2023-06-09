// Filipe Cavalcanti 2023
#ifndef SRC_WEATHER_SERVICE_HPP_
#define SRC_WEATHER_SERVICE_HPP_
#include <iostream>
#include <cmath>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include "observer.hpp"
#include "subject.hpp"

#define TEMPERATURE_IIO_PATH "/sys/bus/iio/devices/iio:device0/in_temp_input"
#define PRESSURE_IIO_PATH "/sys/bus/iio/devices/iio:device0/in_pressure_input"

class WeatherStation : public Subject {
 public:
  explicit WeatherStation(float station_altitude);
  ~WeatherStation() = default;
  void RegisterObserver(Observer *observer) override;
  void RemoveObserver(Observer *observer) override;
  void NotifyObservers() override;
  void UpdateStation();
  float GetTemperature();
  float GetPressure();
 private:
  std::vector<Observer*> observers_;
  float station_altitude_;
  float temperature_;
  float humidity_;
  float pressure_;
  float ConvertToRelativePressure(float pressure, float altitude,
                                  float temperature);
  std::string ReadLineFromFile(const char *filename);
};

#endif  // SRC_WEATHER_SERVICE_HPP_
