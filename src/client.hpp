// Filipe Cavalcanti 2023
#ifndef SRC_CLIENT_HPP_
#define SRC_CLIENT_HPP_
#include <string>
#include <iostream>
#include "observer.hpp"
#include "weather_service.hpp"

class Client : public Observer {
  public:
    /*
     * Generic client which extends Observer.
     * This could be any user implementation that requires data
     * from the station.
     */
    Client(const char* name, WeatherStation* station);
    ~Client();
    void update(float temperature, float humidity, float pressure) override;
    std::string Display();
    std::string client_name;
 private:
    float temperature_;
    float humidity_;
    float pressure_;
    WeatherStation* station_;
};

#endif  // SRC_CLIENT_HPP_
