// Filipe Cavalcanti 2023
#ifndef SRC_OBSERVER_HPP_
#define SRC_OBSERVER_HPP_

#include "common.hpp"

class Observer {
 public:
  /*
   * Observer interface.
   */
   virtual void Update(WeatherStationData* data) = 0;
   virtual ~Observer() = default;
};

#endif  // SRC_OBSERVER_HPP_
