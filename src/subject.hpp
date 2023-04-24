// Filipe Cavalcanti 2023
#ifndef SRC_SUBJECT_HPP_
#define SRC_SUBJECT_HPP_
#include "observer.hpp"

class Subject  {
 public:
  /*
   * Add a new observer to the observer list.
   */
  virtual void RegisterObserver(Observer *observer) = 0;
  /*
   * Remove an observer from the observer list.
   */
  virtual void RemoveObserver(Observer *observer) = 0;
  /*
   * Notify all registered observers when the subject state changes.
   */
  virtual void NotifyObservers() = 0;
  virtual ~Subject() = default;
};


#endif  // SRC_SUBJECT_HPP_
