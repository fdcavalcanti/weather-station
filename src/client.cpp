// Filipe Cavalcanti 2023
#include "client.hpp"

Client::Client(const char* name, WeatherStation* station) {
  client_name = std::string(name);
  station_ = station;
  station_->RegisterObserver(this);
}

Client::~Client() {
  station_->RemoveObserver(this);
}

void Client::update(float temperature, float humidity, float pressure) {
  temperature_ = temperature;
  humidity_ = humidity;
  pressure_ = pressure;
  this->Display();
}

void Client::Display() {
  std::cout << client_name << ": " << temperature_ << ", " << pressure_ << std::endl;
}
