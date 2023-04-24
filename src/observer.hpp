// Filipe Cavalcanti 2023
#ifndef SRC_OBSERVER_HPP_
#define SRC_OBSERVER_HPP_

class Observer {
 public:
  /*
   * Observer interface.
   */
   virtual void update(float temperature, float humidity, float pressure) = 0;
   virtual ~Observer() = default;
};

#endif  // SRC_OBSERVER_HPP_
