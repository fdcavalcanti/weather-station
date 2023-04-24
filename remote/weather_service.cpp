#include <iostream>
#include <cmath>
#include <fstream>
#include <string>

#define TEMPERATURE_IIO_PATH "/sys/bus/iio/devices/iio:device0/in_temp_input"
#define PRESSURE_IIO_PATH "/sys/bus/iio/devices/iio:device0/in_pressure_input"
#define LOCAL_ALTITUDE 685  // Location height relative to sea level

class WeatherStation {
 public:
	WeatherStation(float station_altitude) : station_altitude_(station_altitude) {}
  float GetTemperature();
  float GetPressure();
 private:
  float station_altitude_;
  std::string ReadLineFromFile(const char *filename);
  float ConvertToRelativePressure(float pressure, float height, float temperature);  
};


std::string WeatherStation::ReadLineFromFile(const char *filename) {
  std::ifstream file(filename);
  std::string data;
  if (file.is_open()) {
    std::getline(file, data);
    file.close();
    return data;
  }
  else {
    std::cout << "Error opening file" << std::endl;
    return std::string("Error");
  }
}

float WeatherStation::ConvertToRelativePressure(float pressure, float height, float temperature) {
  float rel_pres = pressure*pow(1 - (0.0065*height)/(temperature+0.0065*height+273.15),  -5.257);
  return rel_pres;
}

float WeatherStation::GetTemperature() {
  std::string raw_temp = this->ReadLineFromFile(TEMPERATURE_IIO_PATH);
  float temperature_c = std::stof(raw_temp) / 1000;
  return temperature_c;
}

float WeatherStation::GetPressure() {
  std::string raw_pressure = this->ReadLineFromFile(PRESSURE_IIO_PATH);
  float abs_pressure = std::stof(raw_pressure) * 10;
  float temperature = this->GetTemperature();
  float rel_pressure = this->ConvertToRelativePressure(abs_pressure, this->station_altitude_, temperature);
  return rel_pressure;
}

int main() {
  WeatherStation *ws = new WeatherStation(LOCAL_ALTITUDE);
  float temp = ws->GetTemperature();
  std::cout << "Temperature C: " << temp << std::endl;
  float pressure = ws->GetPressure();
  std::cout << "Pressure hPa: " << pressure << std::endl;
  return 0;
}
