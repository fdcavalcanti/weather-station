// Filipe Cavalcanti 2023
#ifndef OBSERVER_HPP_
#define OBSERVER_HPP_

class Observer {
 public:
  /*
   * Observer interface.
   */
   virtual void update(float temperature, float humidity, float pressure) = 0;
   virtual ~Observer() = default;
};

#endif  // OBSERVER_HPP_
