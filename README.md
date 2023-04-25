# Real Weather Station - Observer Pattern
This repository contains a real weather station implemented on a Raspberry Pi as a mean to study the Observer Design Pattern.

The Raspberry is equipped with a BMP280 sensor that provides current temperature and pressure, available through its own driver as an IIO Device. This information is read by the Weather Station and made available for all observers.

The Observer Pattern was implemented using the examples from the book Head First Design Patterns, 2nd Edition, Chapter 2.

## Running Locally

After cloning on the Raspberry Pi, compile the shared library with the build script.
```bash
$ ./build.sh
```

Test if the sensor is working by running a sample program. It should create a Weather Station instance, register two observers and notify them with current temperature and pressure.

```bash
$ ./build/main
Weather Station initialized. Altitude: 685 m
Registering new observer: 0x16b4c8
Registering new observer: 0x16b508
Notifying observers
Client 1: 26.6, 1017.37
Client 2: 26.6, 1017.37
Removing observer
Removing observer
```
