// Filipe Cavalcanti 2023
#ifndef SRC_CLIENT_HPP_
#define SRC_CLIENT_HPP_
#include <string>
#include <iostream>
#include "observer.hpp"
#include "weather_service.hpp"

class Client : public Observer {
  public:
    Client(const char* name, WeatherStation* station);
    ~Client();
    void update(float temperature, float humidity, float pressure) override;
    void Display();
    std::string name;
 private:
    float temperature_;
    float humidity_;
    float pressure_;
    WeatherStation* station_;
};

#endif  // SRC_CLIENT_HPP_
