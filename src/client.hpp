// Filipe Cavalcanti 2023
#ifndef SRC_CLIENT_HPP_
#define SRC_CLIENT_HPP_
#include <iostream>
#include <string>

#include "observer.hpp"
#include "weather_service.hpp"

class Client : public Observer {
 public:
  /*
   * Generic client which extends Observer.
   * This could be any user implementation that requires data
   * from the station.
   */
  Client(const char* name, WeatherStation* station)
      : client_name_(name), station_(station) {
    station_->RegisterObserver(this);
  }
  ~Client();
  void update(float temperature, float humidity, float pressure) override;
  std::string Display();

 private:
  float temperature_;
  float humidity_;
  float pressure_;
  std::string client_name_;
  WeatherStation* station_;
};

#endif  // SRC_CLIENT_HPP_
