#ifndef SRC_COMMON_HPP_
#define SRC_COMMON_HPP_

enum Sensor {DHT22, BMP280};

struct WeatherStationData {
  float temperature_dht22;
  float temperature_bmp280;
  float relative_pressure;
  float relative_humidity;
};

#endif  // SRC_COMMON_HPP_
