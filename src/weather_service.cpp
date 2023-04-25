#include "weather_service.hpp"
#define LOCAL_ALTITUDE 685  // Location height relative to sea level

WeatherStation::WeatherStation(float station_altitude) {
  station_altitude_ = station_altitude;
  temperature_ = 0.0;
  humidity_ = 0.0;
  pressure_ = 0.0;
  std::cout << "Weather Station initialized. Altitude: " << station_altitude_
            << " m" << std::endl;
}

void WeatherStation::RegisterObserver(Observer *observer) {
  std::cout << "Registering new observer: " << observer << std::endl;
  observers_.push_back(observer);
}

void WeatherStation::RemoveObserver(Observer *observer) {
  std::cout << "Removing observer" << std::endl;
  auto position = std::find(observers_.begin(), observers_.end(), observer);
  if (position != observers_.end()) {
    observers_.erase(position);
  } else {
    std::cout << "Observer can not be removed." << std::endl;
  }
}

void WeatherStation::NotifyObservers() {
  std::cout << "Notifying observers" << std::endl;
  for (Observer *obs : observers_) {
    obs->update(temperature_, humidity_, pressure_);
  }
}

std::string WeatherStation::ReadLineFromFile(const char *filename) {
  std::ifstream file(filename);
  std::string data;
  if (file.is_open()) {
    std::getline(file, data);
    file.close();
    return data;
  } else {
    std::cout << "Error opening file" << std::endl;
    return std::string("Error");
  }
}

void WeatherStation::UpdateStation() {
  temperature_ = this->GetTemperature();
  pressure_ = this->GetPressure();
  humidity_ = 0.0;
  this->NotifyObservers();
}

float WeatherStation::ConvertToRelativePressure(float pressure, float height,
                                                float temperature) {
  float rel_pres =
      pressure *
      pow(1 - (0.0065 * height) / (temperature + 0.0065 * height + 273.15),
          -5.257);
  return rel_pres;
}

float WeatherStation::GetTemperature() {
  std::string raw_temp = this->ReadLineFromFile(TEMPERATURE_IIO_PATH);
  float temperature_c;
  try {
    temperature_c = std::stof(raw_temp) / 1000;
  } catch (...) {
    std::cout << "Bad temperature read" << std::endl;
    temperature_c = 0.0;
  }
  return temperature_c;
}

float WeatherStation::GetPressure() {
  std::string raw_pressure = this->ReadLineFromFile(PRESSURE_IIO_PATH);
  float abs_pressure;
  try {
    abs_pressure = std::stof(raw_pressure) * 10;
  } catch (...) {
    std::cout << "Bad pressure read" << std::endl;
    abs_pressure = 0;
  }
  float temperature = this->GetTemperature();
  float rel_pressure = this->ConvertToRelativePressure(
      abs_pressure, this->station_altitude_, temperature);
  return rel_pressure;
}
