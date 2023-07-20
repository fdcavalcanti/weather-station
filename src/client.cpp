// Filipe Cavalcanti 2023
#include "client.hpp"

Client::~Client() { station_->RemoveObserver(this); }

void Client::Update(WeatherStationData* data) {
  temperature_bmp280_ = data->temperature_bmp280;
  temperature_dht22_ = data->temperature_dht22;
  humidity_ = data->relative_humidity;
  pressure_ = data->relative_pressure;
  this->Display();
}

std::string Client::Display() {
  std::string ret =
      std::to_string(temperature_bmp280_) + ", " +
      std::to_string(temperature_dht22_) + ", " +
      std::to_string(pressure_) + ", " +
      std::to_string(humidity_);
  std::cout << client_name_ << ": " << ret << std::endl;
  return ret;
}
