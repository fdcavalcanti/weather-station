// Filipe Cavalcanti 2023
#include "client.hpp"

void Client::update(float temperature, float humidity, float pressure) {
  temperature_ = temperature;
  humidity_ = humidity;
  pressure_ = pressure;
  this->Display();
}

void Client::Display() {
  std::cout << name << ": " << temperature_ << ", " << pressure_ << std::endl;
}
