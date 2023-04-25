# Real Weather Station - Observer Pattern
This repository contains a real weather station implemented on a Raspberry Pi as a mean to study the Observer Design Pattern.

The Raspberry is equipped with a BMP280 sensor that provides current temperature and pressure, available through its own driver as an IIO Device. This information is read by the Weather Station and made available for all observers.

The Observer Pattern was implemented using the examples from the book Head First Design Patterns, 2nd Edition, Chapter 2.
