#include "weather_service.hpp"
#define LOCAL_ALTITUDE 685  // Location height relative to sea level

WeatherStation::WeatherStation(float station_altitude) {
  station_altitude_ = station_altitude;
  temperature_bmp280_ = 0.0;
  temperature_dht22_ = 0.0;
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
    obs->update(temperature_bmp280_, humidity_, pressure_);
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
  float temperature_dht22 = this->GetTemperature(DHT22);
  temperature_bmp280_ = this->GetTemperature(BMP280);
  pressure_ = this->GetPressure();
  float humidity = this->GetHumidity();
  /* This check is necessary due to bad sensor returns. */
  if (static_cast<int>(humidity) != 0)
    humidity_ = humidity;

  if (static_cast<int>(temperature_dht22) != 0)
    temperature_dht22_ = temperature_dht22;

  this->NotifyObservers();
}

float WeatherStation::ConvertToRelativePressure(float pressure, float altitude,
                                                float temperature) {
  float rel_pres =
      pressure *
      pow(1 - (0.0065 * altitude) / (temperature + 0.0065 * altitude + 273.15),
          -5.257);
  return rel_pres;
}

float WeatherStation::GetTemperature(Sensor sensor) {
  float temperature_c;
  std::string raw_temp;

  if (sensor == BMP280) {
    raw_temp = this->ReadLineFromFile(iio_temperature_bmp280_.c_str());
  } else {
    raw_temp = this->ReadLineFromFile(iio_temperature_dht22_.c_str());
  }

  try {
    temperature_c = std::stof(raw_temp) / 1000.0f;
  } catch (...) {
    std::cout << "Bad temperature read" << std::endl;
    temperature_c = 0.0;
  }

  return temperature_c;
}

float WeatherStation::GetPressure() {
  std::string raw_pressure = this->ReadLineFromFile(iio_pressure_.c_str());
  float abs_pressure;
  try {
    abs_pressure = std::stof(raw_pressure) * 10;
  } catch (...) {
    std::cout << "Bad pressure read" << std::endl;
    abs_pressure = 0;
  }
  float temperature = this->GetTemperature(BMP280);
  float rel_pressure = this->ConvertToRelativePressure(
      abs_pressure, station_altitude_, temperature);
  return rel_pressure;
}

float WeatherStation::GetHumidity() {
  std::string raw_humidity = this->ReadLineFromFile(iio_humidity_.c_str());
  float rel_humidity;
  try {
    rel_humidity = std::stof(raw_humidity) / 1000;
  } catch (...) {
    std::cout << "Bad humidity read" << std::endl;
    rel_humidity = 0;
  }
  return rel_humidity;
}
