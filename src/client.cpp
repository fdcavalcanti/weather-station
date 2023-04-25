// Filipe Cavalcanti 2023
#include "client.hpp"

// Client::Client(const char* name, WeatherStation* station) {
//   // client_name_ = std::string(name);
//   // station_ = station;
//   // station_->RegisterObserver(this);
// }

Client::~Client() { station_->RemoveObserver(this); }

void Client::update(float temperature, float humidity, float pressure) {
  temperature_ = temperature;
  humidity_ = humidity;
  pressure_ = pressure;
  this->Display();
}

std::string Client::Display() {
  std::cout << client_name_ << ": " << temperature_ << ", " << pressure_
            << std::endl;
  std::string ret =
      std::to_string(temperature_) + ", " + std::to_string(pressure_);
  return ret;
}
